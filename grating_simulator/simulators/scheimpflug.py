import torch
import numpy as np
import cv2
import matplotlib.pyplot as plt
import json

mm = 1
um = 1000

def evaluate_reprojection_error(K, Kh, R_tilt, H, d0, image_size, num_samples=5):
    """
    Compute reprojection error comparing:
      1) Physical mapping: X1 on original plane -> R_tilt -> Kh -> K -> pixel
      2) Homography mapping: H @ [u,v,1]
    
    Args:
        K (ndarray 3x3): Intrinsic matrix.
        Kh (ndarray 3x3): Plane‑mapping matrix.
        R_tilt (ndarray 3x3): 3D rotation matrix.
        H (ndarray 3x3): Homography matrix K @ Kh @ R_tilt @ K^{-1}.
        d0 (float): Distance from camera center to the original plane.
        image_size (tuple): (width, height) in pixels.
        num_samples (int): Number of samples per axis.
    
    Returns:
        rmse (float): Root Mean Square reprojection error (px).
        max_err (float): Maximum reprojection error (px).
    """
    w, h = image_size
    K_inv = np.linalg.inv(K)
    M = K @ Kh @ R_tilt  # physical projection matrix
    
    errors = []
    for u, v in sample_pixels(w, h, num_samples):
        # 1) compute 3D point X1 on original (flat) plane at distance d0
        d = K_inv @ np.array([u, v, 1.0])
        s = d0 / d[2]
        X1 = d * s  # 3D point in camera coords
        
        # 2) physical projection via M
        p_true_h = M @ X1
        p_true = p_true_h[:2] / p_true_h[2]
        
        # 3) homography projection via H
        p_est_h = H @ np.array([u, v, 1.0])
        p_est = p_est_h[:2] / p_est_h[2]
        
        errors.append(np.linalg.norm(p_true - p_est))
    
    errors = np.array(errors)
    rmse = np.sqrt(np.mean(errors**2))
    max_err = np.max(errors)
    return rmse, max_err


def is_rotation_matrix(R, tol=1e-6):
    """
    1) R이 진정한 회전 행렬인가를 확인합니다.
       - R^T @ R ≈ I
       - det(R) ≈ +1

    Args:
        R (ndarray 3×3): 검증할 행렬
        tol (float): 오차 허용치 (Frobenius 노름 기준)

    Returns:
        is_rot (bool): 회전 행렬이면 True
        orth_error (float): ‖R^T R − I‖
        det_error (float): |det(R) − 1|
    """
    I = np.eye(3)
    orth_error = np.linalg.norm(R.T @ R - I, ord='fro')
    det_error = abs(np.linalg.det(R) - 1.0)
    is_rot = (orth_error < tol) and (det_error < tol)
    return is_rot, orth_error, det_error


def stretch_image_to_square(img):
    h, w = img.shape[:2]
    if h > w:
        img = cv2.resize(img, (h, h))
    else:
        img = cv2.resize(img, (w, w))
    return img

def rotate_image(img, N_deg):
    h, w = img.shape[:2]
    M = cv2.getRotationMatrix2D((w/2, h/2), N_deg, 1)
    return cv2.warpAffine(img, M, (w, h))

def sample_pixels(w, h, num_samples=5):
    """
    Generate a grid of pixel coordinates (u, v) for sampling.
    
    Args:
        w (int): Image width in pixels.
        h (int): Image height in pixels.
        num_samples (int): Number of samples along each axis.
    
    Yields:
        (u, v) tuples of sampled pixel coordinates.
    """
    us = np.linspace(0, w - 1, num_samples)
    vs = np.linspace(0, h - 1, num_samples)
    for u in us:
        for v in vs:
            yield u, v

# ----------------------------------------------------------------------------
# 1) Utility: generate a checkerboard in mask space
def create_mask_checkerboard(rows, cols, square_size_px):
    """
    rows, cols: number of squares
    square_size_px: size of each square in pixels in mask space
    """
    H = rows * square_size_px
    W = cols * square_size_px
    mask = np.ones((H, W), dtype=np.uint8)*64
    for i in range(rows):
        for j in range(cols):
            if (i + j) % 2 == 0:
                mask[i*square_size_px:(i+1)*square_size_px,
                     j*square_size_px:(j+1)*square_size_px] = 255
    return mask



class Scheimpflug_simulator():
    def __init__(self):
        # user input parameters
        self.x_rot_deg = 25
        self.y_rot_deg = 0
        self.pad = 100



    def compute_homography_tilt_KR(self, rx, ry, K):
        """
        Compute the homography for a tilt of N_deg about the x-axis (yz-plane rotation).
        
        Parameters:
            N_deg (float): Tilt angle in degrees.
            
        Returns:
            H (ndarray): 3x3 homography matrix.
        """
        alpha = np.deg2rad(rx)
        beta = np.deg2rad(ry)
        
        # Rotation about x-axis
        K_h = np.array([
            [np.cos(beta)*np.cos(alpha), 0,                           np.sin(beta)*np.cos(alpha)],
            [0,                          np.cos(beta)*np.cos(alpha), -np.sin(alpha)             ],
            [0,                          0,                          1                          ]
        ])

        R_tilt = np.array([
            [np.cos(beta),   np.sin(alpha)*np.sin(beta),  -np.sin(beta)*np.cos(alpha)],
            [0,              np.cos(alpha),                np.sin(alpha)],
            [np.sin(beta),  -np.cos(beta)*np.sin(alpha),   np.cos(beta)*np.cos(alpha)]
        ])
        
        # Homography (assuming no translation)
        H = K @ K_h @ R_tilt @ np.linalg.inv(K)
        return H, K_h, R_tilt 


    def compute_camera_matrix(self, d0, di, pixel_size, w, h):

        # --- Compute focal length (thin lens equation) in mm ---
        f_mm = 1.0 / (1.0/d0 + 1.0/di)

        # --- Convert focal length to pixel units ---
        fx = fy = f_mm / pixel_size

        # --- Define the intrinsic matrix K ---
        cx, cy = w / 2.0, h / 2.0    
        
        K = np.array([
            [fx,  0, cx],
            [ 0, fy, cy],
            [ 0,  0,  1]
        ])
        return K
    
    def load_image(self, bmp_path):
        self.proj_image_bmp = cv2.imread(bmp_path, cv2.IMREAD_GRAYSCALE)
        self.proj_image_float = self.proj_image_bmp.astype(np.float32)        
        self.H, self.W = self.proj_image_float.shape[:2]          

    def load_proj_image_parameters(self, json_path):
        with open(json_path, 'r') as f:
            params = json.load(f)
        self.z0_mm = params['z0_mm']
        self.z1_mm = params['z1_mm']
        self.defocus_z1_mm = params['defocus_z1_mm']                
        self.resized_sampling_width_in_um = params["resized_sampling_width_in_um"] 
        self.pupil_diameter_mm = params["pupil_diameter_mm"]
        

    def update_parameters_json_dict(self, file_path):
        with open(file_path, 'r') as f:
            params = json.load(f)
        for key, value in params.items():
            setattr(self, key, value)
        
    def initialize_optics(self):        
        self.pixel_size_mm = self.resized_sampling_width_in_um * mm/um
        self.d0 = self.z0_mm
        self.di = self.z1_mm + self.defocus_z1_mm
        self.magnification = self.di / self.d0

        self.K = self.compute_camera_matrix(self.d0, self.di, self.pixel_size_mm, self.W, self.H)
        self.homographyMTX, self.K_h, self.R_tilt  = self.compute_homography_tilt_KR(self.x_rot_deg, self.y_rot_deg, K = self.K)


    def check_simulation_condition(self):
        assert self.x_rot_deg < 90 and self.x_rot_deg > -90, 'x_rot_deg should be less than 90 degrees and greater than -90 degrees'
        assert self.y_rot_deg < 90 and self.y_rot_deg > -90, 'y_rot_deg should be less than 90 degrees and greater than -90 degrees'
        assert self.magnification > 0, 'magnification should be greater than 0'
        assert self.d0 > 0, 'd0 should be greater than 0'
        assert self.di > 0, 'di should be greater than 0'
        assert self.pad > 0, 'pad should be greater than 0'

        # 샤임플러그 원리에 따른 물체 공간 각도 계산
        
        object_x_angle = -np.rad2deg(np.arctan(np.tan(np.deg2rad(self.x_rot_deg)) / self.magnification))
        object_y_angle = -np.rad2deg(np.arctan(np.tan(np.deg2rad(self.y_rot_deg)) / self.magnification))

        print('---------------------------------------------------------------------')
        print(f'Your Camera matrix is: \n {self.K}')
        print(f'\nYour Homography matrix is: \n {self.homographyMTX}')
        print(f'\nYour Rotation matrix is: \n\t -> Projection angle in x-axis: {self.x_rot_deg} deg\n\t -> Projection angle in y-axis: {self.y_rot_deg} deg\nRotation matrix: \n {self.R_tilt}')
        print(f'\nYour Relative traslasion matrix according to the rotation matrix is: \n {self.K_h}')
        print()        
        print('---------------------------------------------------------------------')
        
        print('The input values for pin hole model are:')
        print(f'\t-> Focal length: {self.d0} mm')
        print(f'\t-> Working distance: {self.di} mm')
        print(f'\t-> Magnification: {self.di/self.d0}')
        print(f'\t-> Image size: {self.W} x {self.H} pixels')
        print(f'\t-> Pixel size: {self.pixel_size_mm} mm')
        print()
        print('---------------------------------------------------------------------')
        print(f'The output values are:')
        print(f'\t-> Pixel size: {self.pixel_size_mm} mm')
        print(f'\t-> Image size (after removing padding):')
        print(f'\t\t-> {self.W-self.pad*2} x {self.H-self.pad*2} pixels')
        print(f'\t\t-> {self.W*self.pixel_size_mm} x {self.H*self.pixel_size_mm} mm')
        
        print(f'\t-> Scheimpflug angle in image (i.e. projection) space (x-axis): {self.x_rot_deg} deg')
        print(f'\t-> Scheimpflug angle in image (i.e. projection) space (y-axis): {self.y_rot_deg} deg')
        print(f'\t-> Scheimpflug angle in object space (x-axis): {object_x_angle:.2f} deg')
        print(f'\t-> Scheimpflug angle in object space (y-axis): {object_y_angle:.2f} deg')
        print('---------------------------------------------------------------------')

    def apply_homography(self):
        self.warped_image = cv2.warpPerspective(self.proj_image_float, self.homographyMTX   , (self.W, self.H))

    def imshow_result(self):
        pad = self.pad
        self.warped_crop = self.warped_image[pad:self.H-pad,pad:self.W-pad]
        extent_x = np.array([0, self.warped_crop.shape[1]]) * self.pixel_size_mm
        extent_y = np.array([0, self.warped_crop.shape[0]]) * self.pixel_size_mm

        # Create figure with subplots
        fig = plt.figure(figsize=(10, 9))
        gs = plt.GridSpec(2, 2, width_ratios=[3, 1], height_ratios=[3, 1])

        # Main image plot
        ax_main = plt.subplot(gs[0,0])
        im = ax_main.imshow(self.warped_crop, cmap='gray', extent=[extent_x[0], extent_x[1], extent_y[1], extent_y[0]], vmin=0, vmax=255)
        ax_main.set_xlabel('Width (mm)')
        ax_main.set_ylabel('Height (mm)')

        # X cross section
        ax_x = plt.subplot(gs[1,0])
        x_pixels = np.arange(0, self.warped_crop.shape[1])
        x_mm = x_pixels * self.pixel_size_mm
        ax_x.plot(x_mm, self.warped_crop[self.warped_crop.shape[0]//2,:])
        ax_x.set_xlabel('Width (mm)')
        ax_x.set_ylabel('Intensity')
        ax_x.set_ylim(0,255)

        # Y cross section
        ax_y = plt.subplot(gs[0,1])
        y_pixels = np.arange(0, self.warped_crop.shape[0])
        y_mm = y_pixels * self.pixel_size_mm
        ax_y.plot(self.warped_crop[:,self.warped_crop.shape[1]//2], y_mm)
        ax_y.set_xlabel('Intensity')
        ax_y.set_ylabel('Height (mm)')
        ax_y.invert_yaxis()  # Y축 방향 반전
        ax_y.set_xlim(0,255)

        plt.tight_layout()
        plt.show()


    def run(self, bmp_path, json_path, parameters=None):
        self.load_image(bmp_path)
        self.load_proj_image_parameters(json_path)
        if parameters is not None:
            self.update_parameters()    
        self.initialize_optics()
        self.check_simulation_condition()

        self.apply_homography()
        # self.flat_distance_map, self.tilted_distance_map = self.compute_pixel_to_camera_distance_GPU()
        self.compute_pixel_to_camera_distance_and_scale_gpu()
        self.imshow_result()


    def compute_pixel_to_camera_distance_and_scale_gpu(self):
        """
        Compute the distance from each pixel to the camera for both flat and tilted images using d0 and d1,
        and calculate the scale for each pixel using GPU.
        
        Returns:
            flat_distance_map_d0 (ndarray): Distance map for the flat image using d0.
            tilted_distance_map_d0 (ndarray): Distance map for the tilted image using d0.
            flat_distance_map_d1 (ndarray): Distance map for the flat image using d1.
            tilted_distance_map_d1 (ndarray): Distance map for the tilted image using d1.
            scale_map (ndarray): Scale map for each pixel.
        """
        # Initialize distance maps on GPU
        flat_distance_map_d0 = torch.zeros((self.H, self.W), device='cuda')
        tilted_distance_map_d0 = torch.zeros((self.H, self.W), device='cuda')
        flat_distance_map_d1 = torch.zeros((self.H, self.W), device='cuda')
        tilted_distance_map_d1 = torch.zeros((self.H, self.W), device='cuda')
        scale_map = torch.zeros((self.H, self.W), device='cuda')

        # Convert intrinsic matrix to torch tensor and move to GPU
        K_inv = torch.tensor(np.linalg.inv(self.K), device='cuda', dtype=torch.float32)

        # Create a grid of pixel coordinates
        u, v = torch.meshgrid(torch.arange(self.W, device='cuda'), torch.arange(self.H, device='cuda'))
        u = u.t().reshape(-1)
        v = v.t().reshape(-1)

        # Calculate distances for flat image using d0
        d = torch.stack([u, v, torch.ones_like(u)], dim=1).float()
        d = torch.matmul(d, K_inv.t())
        s_d0 = self.d0 / d[:, 2]
        X1_d0 = d * s_d0.unsqueeze(1)
        flat_distance_map_d0 = torch.norm(X1_d0, dim=1).reshape(self.H, self.W)

        # Calculate distances for flat image using d1
        s_d1 = self.di / d[:, 2]
        X1_d1 = d * s_d1.unsqueeze(1)
        flat_distance_map_d1 = torch.flip(torch.norm(X1_d1, dim=1).reshape(self.H, self.W), dims=[0])

        # Calculate distances for tilted image using d0
        homographyMTX_inv = torch.tensor(np.linalg.inv(self.homographyMTX), device='cuda', dtype=torch.float32)
        p_est_h = torch.matmul(torch.stack([u, v, torch.ones_like(u)], dim=1).float(), homographyMTX_inv.t())
        p_est = p_est_h[:, :2] / p_est_h[:, 2].unsqueeze(1)

        d = torch.stack([p_est[:, 0], p_est[:, 1], torch.ones_like(p_est[:, 0])], dim=1)
        d = torch.matmul(d, K_inv.t())
        s_d0 = self.d0 / d[:, 2]
        X1_d0 = d * s_d0.unsqueeze(1)
        tilted_distance_map_d0 = torch.norm(X1_d0, dim=1).reshape(self.H, self.W)

        # Calculate distances for tilted image using d1
        s_d1 = self.di / d[:, 2]
        X1_d1 = d * s_d1.unsqueeze(1)
        tilted_distance_map_d1 = torch.flip(torch.norm(X1_d1, dim=1).reshape(self.H, self.W), dims=[0])

        # Calculate scale map
        flat_scale_map = flat_distance_map_d1 / flat_distance_map_d0
        tilted_scale_map = tilted_distance_map_d1 / tilted_distance_map_d0
        
        # Calculate f# map
        flat_f_num_map = self.pupil_diameter_mm/ flat_distance_map_d0
        tilted_f_num_map = self.pupil_diameter_mm/ tilted_distance_map_d0
        
        # Calculate brightness attenuation as a function of distance (scale) by point.        
        inv_sqr_raw = 1/tilted_scale_map**2
        inv_sqr_raw /= torch.max(inv_sqr_raw)

        # Calculate brightness attenuation as a function of cos**4 raw
        d_norm = d / torch.norm(d, dim=1, keepdim=True)  # Normalize direction vectors
        # Calculate cos(theta) for each pixel
        cos_theta = d_norm[:, 2]  # z-component of the normalized direction vector
        attenuation_map = cos_theta**4
        attenuation_map = attenuation_map.reshape(self.H, self.W)
        
        # results
        self.inv_sqr_raw = inv_sqr_raw.cpu().numpy()
        self.attenuation_map = attenuation_map.cpu().numpy()





# img = create_mask_checkerboard(5, 5, square_size_px=500) # 25MP sensor
# cv2.imwrite("test_checkerboard.bmp", img)
target_img_path = './20M20um/27um/defocused_projected_image.bmp'
proj_json_path = './20M20um/27um/Projection_params.json'
new_img_path = target_img_path.replace('.bmp','_squre.bmp')
img = cv2.imread(target_img_path, cv2.IMREAD_GRAYSCALE)
img = stretch_image_to_square(img)
img = rotate_image(img, 0)
cv2.imwrite(new_img_path, img)

ss = Scheimpflug_simulator()
ss.x_rot_deg = 2.576
ss.y_rot_deg = 0
ss.pad = 500
ss.run(bmp_path=new_img_path, json_path=proj_json_path)
final_output = ss.inv_sqr_raw*ss.attenuation_map*ss.warped_image
final_output = ss.inv_sqr_raw*ss.warped_image

fig, ax = plt.subplots(1,3, sharex=True, sharey=True)
ax[0].imshow(ss.inv_sqr_raw, vmin=0, vmax=1, cmap = 'jet')
ax[1].imshow(ss.attenuation_map, vmin=0, vmax=1, cmap = 'jet')
ax[2].imshow(final_output, cmap='gray')

'''
        return (flat_distance_map_d0.cpu().numpy(), tilted_distance_map_d0.cpu().numpy(),
                flat_distance_map_d1.cpu().numpy(), tilted_distance_map_d1.cpu().numpy(),
                scale_map.cpu().numpy())
'''
cv2.imwrite(new_img_path.replace('.bmp','_warp.bmp'), ss.warped_image.astype(np.uint8))
cv2.imwrite(new_img_path.replace('.bmp','_warp_var_brightness.bmp'), final_output)







# 1) R_tilt 검증
is_rot, ort_err, det_err = is_rotation_matrix(ss.R_tilt)
print(f"Rotation matrix? {is_rot}, orthogonality error={ort_err:.2e}, det error={det_err:.2e}")

rmse, max_err = evaluate_reprojection_error(
    K=ss.K,
    Kh=ss.K_h,
    R_tilt=ss.R_tilt,
    H=ss.homographyMTX,
    d0=ss.d0,
    image_size=(ss.W, ss.H),
    num_samples=9
)
print(f"RMSE: {rmse:.3f} px, Max Error: {max_err:.3f} px")

