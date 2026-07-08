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
        self.header_prefix = ''



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
        if hasattr(self, 'final_result') and self.final_result is not None:
            img = self.final_result
        else:
            img = self.warped_image
        img_crop = img[pad:self.H-pad, pad:self.W-pad]
        extent_x = np.array([0, img_crop.shape[1]]) * self.pixel_size_mm
        extent_y = np.array([0, img_crop.shape[0]]) * self.pixel_size_mm

        fig = plt.figure(figsize=(10, 9))
        gs = plt.GridSpec(2, 2, width_ratios=[3, 1], height_ratios=[3, 1])

        ax_main = plt.subplot(gs[0, 0])
        ax_main.imshow(img_crop, cmap='gray', extent=[extent_x[0], extent_x[1], extent_y[1], extent_y[0]], vmin=0, vmax=255)
        ax_main.set_xlabel('Width (mm)')
        ax_main.set_ylabel('Height (mm)')

        ax_x = plt.subplot(gs[1, 0])
        x_mm = np.arange(img_crop.shape[1]) * self.pixel_size_mm
        ax_x.plot(x_mm, img_crop[img_crop.shape[0] // 2, :])
        ax_x.set_xlabel('Width (mm)')
        ax_x.set_ylabel('Intensity')
        ax_x.set_ylim(0, 255)

        ax_y = plt.subplot(gs[0, 1])
        y_mm = np.arange(img_crop.shape[0]) * self.pixel_size_mm
        ax_y.plot(img_crop[:, img_crop.shape[1] // 2], y_mm)
        ax_y.set_xlabel('Intensity')
        ax_y.set_ylabel('Height (mm)')
        ax_y.invert_yaxis()
        ax_y.set_xlim(0, 255)

        plt.tight_layout()
        return fig


    def run(self, bmp_path, json_path, parameters=None):
        self.load_image(bmp_path)
        self.load_proj_image_parameters(json_path)
        if parameters is not None:
            self.update_parameters()
        self.initialize_optics()
        self.check_simulation_condition()

        self.apply_homography()
        self.compute_pixel_to_camera_distance_and_scale()
        self.final_result = self.inv_sqr_raw * self.attenuation_map * self.warped_image
        self.imshow_result()


    def compute_pixel_to_camera_distance_and_scale(self, progress_callback=None):
        """역 호모그래피의 야코비안 행렬식으로 Scheimpflug 배율 변화에 의한 밝기 감쇠를 계산.

        |det(J_{H^{-1}})| = 로컬 면적 스케일링 = 1/M_local² (정규화 후).
        x축 회전만 있을 때 (y_rot=0): w = H_inv[2,1]*v + H_inv[2,2] → 행 방향만 변화.
        """
        print("Computing brightness attenuation (Jacobian method)...")

        if progress_callback:
            progress_callback(0, 2, "Jacobian of inverse homography")

        H_inv = np.linalg.inv(self.homographyMTX)
        h = H_inv.astype(np.float64)

        u_arr = np.arange(self.W, dtype=np.float64)
        v_arr = np.arange(self.H, dtype=np.float64)
        uu, vv = np.meshgrid(u_arr, v_arr)

        w = h[2, 0] * uu + h[2, 1] * vv + h[2, 2]
        x_p = h[0, 0] * uu + h[0, 1] * vv + h[0, 2]
        y_p = h[1, 0] * uu + h[1, 1] * vv + h[1, 2]
        u_p = x_p / w
        v_p = y_p / w

        du_du = (h[0, 0] - u_p * h[2, 0]) / w
        du_dv = (h[0, 1] - u_p * h[2, 1]) / w
        dv_du = (h[1, 0] - v_p * h[2, 0]) / w
        dv_dv = (h[1, 1] - v_p * h[2, 1]) / w

        det_J = du_du * dv_dv - du_dv * dv_du

        inv_sqr_raw = np.abs(det_J)
        inv_sqr_raw /= np.max(inv_sqr_raw)
        self.inv_sqr_raw = inv_sqr_raw.astype(np.float32)

        if progress_callback:
            progress_callback(1, 2, "Computing cos⁴θ (reference)")

        # cos⁴θ natural vignetting — 기하학적 cos⁴θ (Lambert + solid angle + off-axis distance).
        # macro lens의 FoV가 작으므로 효과는 미약하나, inv_sqr_raw와 함께 final_result에 적용.
        K_inv = np.linalg.inv(self.K).astype(np.float64)
        p_flat = np.stack([u_p.ravel(), v_p.ravel(), np.ones(self.H * self.W)], axis=1)
        d = p_flat @ K_inv.T
        d_norm = d / np.linalg.norm(d, axis=1, keepdims=True)
        self.attenuation_map = (d_norm[:, 2] ** 4).reshape(self.H, self.W).astype(np.float32)

        if progress_callback:
            progress_callback(2, 2, "Done")

    # keep old name as alias
    compute_pixel_to_camera_distance_and_scale_gpu = compute_pixel_to_camera_distance_and_scale

    def save_image(self, output_dir=None):
        import os
        prefix = self.header_prefix

        def _path(name):
            return os.path.join(output_dir, prefix + name) if output_dir else prefix + name

        if hasattr(self, 'warped_image') and self.warped_image is not None:
            cv2.imwrite(_path('warped_image.bmp'), self.warped_image.astype(np.uint8))
        if hasattr(self, 'final_result') and self.final_result is not None:
            cv2.imwrite(_path('scheimpflug_final_result.bmp'), self.final_result.astype(np.uint8))
        print(f"Scheimpflug images saved to {output_dir or '.'}")

    def save_parameters_json_dict(self, json_path):
        params = {
            'x_rot_deg': self.x_rot_deg,
            'y_rot_deg': self.y_rot_deg,
            'pad': self.pad,
        }
        if hasattr(self, 'z0_mm'):
            params['z0_mm'] = self.z0_mm
            params['z1_mm'] = self.z1_mm
            params['defocus_z1_mm'] = self.defocus_z1_mm
            params['resized_sampling_width_in_um'] = self.resized_sampling_width_in_um
            params['pupil_diameter_mm'] = self.pupil_diameter_mm
        with open(json_path, 'w') as f:
            json.dump(params, f, indent=4)
        print(f"Parameters saved to {json_path}")




# --- Utility functions migrated from bin/20M20um/ standalone scripts ---

def convert_angles(angle_value_deg, magnification, mode='to_projection'):
    angle_rad = np.radians(angle_value_deg)
    if mode == 'to_projection':
        return np.degrees(np.arctan(np.tan(angle_rad) / magnification))
    elif mode == 'to_scheimpflug':
        return np.degrees(np.arctan(magnification * np.tan(angle_rad)))
    else:
        raise ValueError("mode must be 'to_projection' or 'to_scheimpflug'")



def add_poisson_noise(image):
    return np.random.poisson(image).astype(np.uint8)

def add_gaussian_noise(image, mean=0, std=1):
    gaussian_noise = np.random.normal(mean, std, image.shape)
    return np.clip(image + gaussian_noise, 0, 255).astype(np.uint8)

def add_speckle_noise(image, std_factor=0.1):
    noise = np.random.randn(*image.shape) * std_factor
    return np.clip(image + image * noise, 0, 255).astype(np.uint8)

def estimate_sine_wave_params(image):
    hist, bins = np.histogram(image.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    min_val = np.min(bins[np.where(cdf > 0.1 * cdf[-1])])
    max_val = np.max(bins[np.where(cdf < 0.997 * cdf[-1])])
    return min_val, max_val

def normalize_sim_image(sim_img, min_val, max_val):
    sim_img_normalized = (sim_img - np.min(sim_img)) / (np.max(sim_img) - np.min(sim_img))
    sim_img_normalized = sim_img_normalized * (max_val - min_val) + min_val
    return sim_img_normalized

def find_crop_region(sim_img, exp_img):
    result = cv2.matchTemplate(sim_img, exp_img, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    start_x, start_y = max_loc
    end_x = start_x + exp_img.shape[1]
    end_y = start_y + exp_img.shape[0]
    return start_x, start_y, end_x, end_y, max_val

