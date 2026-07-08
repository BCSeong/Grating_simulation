# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 21:47:09 2025

@author: Z4G5
"""

#%% Tab2
m = 1/1000
mm = 1
um = 1000



import numpy as np
from matplotlib import pyplot as plt
import cv2
import json
from tqdm import tqdm

# 격자를 현미경으로 관찰한 이미지 결과를 모사합니다
def myFFT(ndarray):
    FT = np.fft.fftshift(np.fft.fftn(np.fft.ifftshift(ndarray)))
    return FT
def myiFFT(ndarray):
    iFT = np.fft.fftshift(np.fft.ifftn(np.fft.ifftshift(ndarray)))
    return iFT

class Projection_image_simulator():
    def __init__(self):
        self.debug_mode:bool = False
        # default user parameters
        # general parameters
        self.mask_path:str = ''
        self.header_prefix:str = ''
        self.save_result_toggle:bool = True
        # projection parameter
        self.z0_mm:float = 31.5
        self.z1_mm:float = 630.0
        self.pupil_diameter_mm:float = 2.0
        self.defocus_z1_mm:float = 1.0        
        self.resize_factor:float = 1.0
        self.resize_factor_along_width:float = 1.0
        # projection + clear boarder
        self.clear_board_toggle:bool = True
        self.clear_board_factor:float = 1.0
        
        

        # custom image property parameters
        self.custom_image_property:bool = False
        self.mask_sampling_width_in_um:float = 0.05        
        # custom spectrum parameters
        self.custom_spectrum_toggle:bool = False
        self.spectrum_min:float = 0.5876         
        self.spectrum_max:float = 0.5876         
        self.spectrum_step:float = 0.0         
        self.wvls_um:list = [0.5876]
        
                

        # loaded image review parameters
        self.H:int = 0
        self.W:int = 0
        self.H_mm:float = 0
        self.W_mm:float = 0
        # custom image property parameters
        self.custom_image_property_toggle:bool = False
        self.mask_sampling_width_in_um:float = 0
        self.period_of_saw:float = 0
        
        # default review parameters
        self.obj_space_f_number:float = 0.0
        self.img_space_na:float = 0.0
        self.magnification_defo:float = 0        

        self.projection_H_mm:float = 0
        self.projection_W_mm:float = 0        
        self.projection_sampling_width_in_um:float = 0

        # resized review parameters
        self.resized_sampling_width_in_um:float = 0
        self.resized_H:int = 0
        self.resized_W:int = 0
        self.resized_H_mm:float = 0
        self.resized_W_mm:float = 0

        # results
        self.mask_float = None        
        self.mask_bmp = None
        self.eff_OTF_uint = None
        self.eff_defocus_OTF_uint = None
        self.projected_mask_uint = None
        self.defocused_projected_mask_uint = None
        self.resized_result_uint = None
        self.psf_crs_uint = None
        self.eff_Phi_angle_uint = None
   
    def save_parameters_json_dict(self, json_path = None):
        """현재 파라미터를 JSON 파일로 저장"""
        
        if json_path is None:
            json_path = self.header_prefix + 'Projection_params.json'
        
        params = {
            # general parameters
            'header_prefix' : self.header_prefix,
            # projection parameter
            'z0_mm' : self.z0_mm,
            'z1_mm' : self.z1_mm,
            'pupil_diameter_mm' : self.pupil_diameter_mm,
            'defocus_z1_mm' : self.defocus_z1_mm,
            'resize_factor' : self.resize_factor,
            'resize_factor_along_width' : self.resize_factor_along_width,
            # projection + clear boarder
            'clear_board_toggle' : self.clear_board_toggle,
            'clear_board_factor' : self.clear_board_factor,
            # custom image property parameters
            'custom_image_property_toggle' : self.custom_image_property_toggle,
            'mask_sampling_width_in_um' : self.mask_sampling_width_in_um,
            'period_of_saw' : self.period_of_saw,
            # custom spectrum parameters
            'custom_spectrum_toggle' : self.custom_spectrum_toggle,
            'spectrum_min' : self.spectrum_min,
            'spectrum_max' : self.spectrum_max,
            'spectrum_step' : self.spectrum_step,


            # review parameters for reference
            'obj_space_f_number' : self.obj_space_f_number,
            'img_space_na' : self.img_space_na,
            'magnification_defo' : self.magnification_defo,
            'projection_H_mm' : self.projection_H_mm,
            'projection_W_mm' : self.projection_W_mm,
            'projection_sampling_width_in_um' : self.projection_sampling_width_in_um,
            # resized review parameters
            'resized_sampling_width_in_um' : self.resized_sampling_width_in_um,
            'resized_H' : self.resized_H,
            'resized_W' : self.resized_W,
            'resized_H_mm' : self.resized_H_mm,
            'resized_W_mm' : self.resized_W_mm
            }

        with open(json_path, 'w') as f:
            json.dump(params, f, indent=4)
        print(f"Parameters saved to {json_path}")


    
    def update_parameters_json_dict(self, file_path):
        with open(file_path, 'r') as f:
            params = json.load(f)
        for key, value in params.items():
            setattr(self, key, value)
                
    def load_image(self, bmp_path):
        self.mask_bmp = cv2.imread(bmp_path, cv2.IMREAD_GRAYSCALE)
        self.mask_float = self.mask_bmp.astype(np.float32)        
        self.H = self.mask_float.shape[0]
        self.W = self.mask_float.shape[1]        
        
    def load_grating_parameters(self, json_path):
        with open(json_path, 'r') as f:
            params = json.load(f)
        self.mask_sampling_width_in_um = params['mask_sampling_width_in_um']
        self.period_of_saw = params['period_of_saw']
        


    def initialize_optics(self):        
        assert self.H != 0 and self.W != 0 and self.mask_float is not None, 'Image is not defined correctly, load gray image first'
        assert self.mask_sampling_width_in_um != 0, 'mask_sampling_width_in_um is not defined, load grating parameters first or set custom image property'
        
        self.H_mm = self.H*self.mask_sampling_width_in_um
        self.W_mm = self.W*self.mask_sampling_width_in_um
        self.magnification_defo = (self.z1_mm +self. defocus_z1_mm )/self.z0_mm # mask is magnified by M (ex z1=600 z2 = 30, M = 20)
        self.obj_space_f_number = 0.5/((self.pupil_diameter_mm/2)/self.z0_mm)
        self.img_space_na = (self.pupil_diameter_mm/2)/self.z1_mm
        self.DOF_bidirec_mm = (self.wvls_um[int(len(self.wvls_um)/2)]*mm/um)/self.img_space_na**2
        
        # TODO: clear baord after resize
        if self.clear_board_toggle:
            self.board_crop_px = int(self.period_of_saw/self.mask_sampling_width_in_um*self.clear_board_factor)            
            self.W_crop = int(self.W-self.board_crop_px*2)
        else:
            self.W_crop = self.W
            

        self.projection_sampling_width_in_um = self.mask_sampling_width_in_um*self.magnification_defo
        self.projection_H_mm = self.H*self.projection_sampling_width_in_um *mm/um
        self.projection_W_mm = self.W_crop*self.projection_sampling_width_in_um *mm/um
        '''
        # version 2 : block_reduce parameters   
        self.resized_H = self.H//self.resize_factor
        self.resized_W = self.W_crop//self.resize_factor_along_width
        self.resized_sampling_width_in_um = self.projection_sampling_width_in_um*(self.resize_factor)
        self.resized_sampling_width_in_um_along_width = self.projection_sampling_width_in_um*(self.resize_factor_along_width)
        self.resized_H_mm = self.resized_H * self.resized_sampling_width_in_um *mm/um
        self.resized_W_mm = self.resized_W * self.resized_sampling_width_in_um_along_width *mm/um
        
        '''
        # version 1 : cv2.resize parameters
        self.resized_H = self.H//self.resize_factor
        self.resized_W = self.W_crop//self.resize_factor_along_width
        self.resized_sampling_width_in_um = self.projection_sampling_width_in_um*(self.H/self.resized_H)
        self.resized_sampling_width_in_um_along_width = self.projection_sampling_width_in_um*(self.W/self.resized_W)
        self.resized_H_mm = self.resized_H * self.resized_sampling_width_in_um *mm/um
        self.resized_W_mm = self.resized_W * self.resized_sampling_width_in_um_along_width *mm/um
        

        # projection space
        prj_x = (np.arange(self.W)-self.W/2)*self.projection_sampling_width_in_um
        prj_y = (np.arange(self.H)-self.H/2)*self.projection_sampling_width_in_um
        # prj_X, prj_Y = np.meshgrid(prj_x, prj_y)

        # frequency space
        self.dky = 1/(self.H*self.projection_sampling_width_in_um)
        self.dkx = 1/(self.W*self.projection_sampling_width_in_um)
        kx = (np.arange(self.W) - self.W/2)*self.dkx
        ky = (np.arange(self.H) - self.H/2)*self.dky
        # Create the 2D grid    
        KX, KY = np.meshgrid(kx, ky)
        self.RHO = np.sqrt(KX**2+KY**2)

    def check_simulation_condition(self):
        min_cf = self.img_space_na/np.min(self.wvls_um)
        check1 = min_cf < np.max(self.RHO)/5
        assert check1, 'NA is too large / sampling size of input image is too small'
        max_cf = self.img_space_na/np.max(self.wvls_um)
        check2 = max_cf > min(self.dkx, self.dky)*4
        assert check2, 'NA is too small / sampling size of input image is too large'
        crit = check1 and check2 # pass of fail

        # assert self.resize_factor%1 == 0, 'resize_factor (height) must be an integer'
        # assert self.resize_factor_along_width%1 == 0, 'resize_factor (width) must be an integer'
        # self.resize_factor = int(self.resize_factor)
        # self.resize_factor_along_width = int(self.resize_factor_along_width)
        assert self.resize_factor > 0, 'resize_factor (height) must be positive'
        assert self.resize_factor_along_width > 0, 'resize_factor (width) must be positive'
        
        
        print('---------------------------------------------------------------------')
        print(f'* Cut off frequency, NA/lambda : {min_cf:.2f} um^-1 to {max_cf:.2f} um^-1')
        print(f'* Defiend Max Value in frequency domain, f_max : {np.max(self.RHO):.2f} um^-1')
        print('* Cut off frequency should be less than f_max/5 (Nyquist condition assuming OTF)')
        print(f'* Sampling size of frequency domain : {self.dkx:.4f} um^-1 (dkx), {self.dky:.4f} um^-1 (dky)')
        print(f'\t->Simulation Condition Check: {"Pass" if crit else "Fail"}')
        print()
        
        
        print('---------------------------------------------------------------------')
        print(f'Calcurated Depth of Field : +-{self.DOF_bidirec_mm/2:.4f} mm')
        print()

    def calculate_OTF(self, user_z1_defo_mm=None, disable_tqdm=False, progress_callback=None):
        # -----------------------------------------------------------------------------
        # Defocus propagation phase term for FFT-based simulation
        #
        # We use numpy's FFT (np.fft.fftn / np.fft.ifftn), which defines the
        # forward transform as:
        #
        #   F[k] = ∑ₙ f[n] * exp(-2πi * (k·n)/N)
        #
        # and the corresponding frequency grid (KX, KY) is in "cycles per unit
        # distance" (here cycles per µm), NOT angular frequency ω = 2π·ν.
        #
        # In paraxial wave optics, the defocus transfer function in spatial-frequency
        # domain ν (cycles/length) is derived as:
        #
        #   H(ν) = exp[- i · π · λ · z · (ν²) ]
        #
        # where
        #   λ = wavelength [µm],
        #   z = defocus distance [µm],
        #   ν = spatial frequency [cycles/µm].
        #
        # Notice there is only a single π in the exponent. If you instead wrote
        #
        #   exp[- i · 2π · λ · z · (ν²)]
        #
        # you would double the intended phase curvature and produce an incorrect PSF/OTF.
        #
        # Therefore, when using numpy FFT with KX, KY defined as:
        #
        #   dkx = 1.0 / (W * dx)      # cycles per µm
        #   kx = (arange(W) - W/2) * dkx
        #   KX, KY = meshgrid(kx, ky)
        #
        # the correct defocus phase filter is:
        #
        #   # lambda_um: wavelength in µm
        #   # dz_um:   defocus distance in µm
        #   # KX, KY: spatial frequency grids in cycles/µm
        #   Phi = np.exp(
        #       -1j * np.pi * lambda_um * dz_um * (KX**2 + KY**2)
        #   )
        #
        # Explanation of each term:
        #  - np.pi             : matches the "π" in the analytic H(ν) expression.
        #  - lambda_um * dz_um : λ·z gives units of µm², canceling the µm⁻² from ν².
        #  - (KX**2 + KY**2)   : squared spatial frequency in (cycles/µm)².
        #
        # This Phi can be multiplied pointwise with your pupil function in frequency
        # domain before taking an inverse FFT to generate the defocused PSF:
        #
        #   psf_def = np.abs(ifftn(pupil * Phi))**2
        #
        # and then FFT(psf_def) yields the exact defocus-included OTF:
        #
        #   otf_def = fftn(psf_def)
        #
        # -----------------------------------------------------------------------------

        OTFs=[]
        defocus_OTFs=[]
        defo_psfs = []
        Phis = []
        n_wvls = len(self.wvls_um)
        for i, lamb_um in enumerate(self.wvls_um):
            if progress_callback and not disable_tqdm:
                progress_callback(i, n_wvls, f"OTF: {lamb_um:.4f} um ({i+1}/{n_wvls})")
            cf = self.img_space_na/lamb_um
            P = (self.RHO <= cf).astype(float)
            # Defocus 용 Phase term
            del_z_um = self.defocus_z1_mm*um/mm if user_z1_defo_mm is None else user_z1_defo_mm*um/mm
            Phi = np.exp(-1j*np.pi * lamb_um * del_z_um * self.RHO**2)
            

            psf = np.abs(myiFFT(P))**2
            defocus_psf = np.abs(myiFFT(P*Phi))**2
            OTF = myFFT(psf)
            defocus_OTF = myFFT(defocus_psf)
            
            
            Phis.append(Phi)
            OTFs.append(OTF)
            defocus_OTFs.append(defocus_OTF)
            defo_psfs.append(defocus_psf)
        
        Phis = np.array(Phis)
        _eff_Phi = np.sum(Phis, axis=0)
        _eff_Phi_angle = np.angle(_eff_Phi)
        _eff_Phi_angle -= _eff_Phi_angle        
        self.eff_Phi_angle_uint = (_eff_Phi_angle/np.max(_eff_Phi_angle)*255).astype(np.uint8)
            
        OTFs = np.array(OTFs)        
        _eff_OTF = np.sum(OTFs, axis=0)
        _norm_focus = np.max(np.abs(_eff_OTF))
        _eff_OTF /= _norm_focus
        self.eff_OTF = _eff_OTF
        self.eff_OTF_uint = (np.abs(self.eff_OTF) / np.max(np.abs(self.eff_OTF)) * 255).astype(np.uint8)

        defocus_OTFs = np.array(defocus_OTFs)
        _eff_defocus_OTF = np.sum(defocus_OTFs, axis=0)
        _eff_defocus_OTF /= _norm_focus # devided by ideal OTF energy
        self.eff_defocus_OTF = _eff_defocus_OTF
        self.eff_defocus_OTF_uint = (np.abs(self.eff_defocus_OTF) / np.max(np.abs(self.eff_defocus_OTF)) * 255).astype(np.uint8)

        # check psfs for debuging
        defo_psfs = np.array(defo_psfs)
        _eff_defo_psf = np.sum(defo_psfs, axis=0)        
        self.eff_defo_psf = _eff_defo_psf
        

    def perform_OTF(self):
        projected_mask = np.abs(myFFT(myiFFT(self.mask_float.astype(np.float32))*self.eff_OTF))
        if self.clear_board_toggle:
            projected_mask = projected_mask[:,self.board_crop_px:-self.board_crop_px]
            assert projected_mask.shape[1] == self.W_crop, "clear board operation error!"
        self.projected_mask_uint = np.clip(projected_mask, 0, 255).astype(np.uint8)

        defocused_projected_mask = np.abs(myFFT(myiFFT(self.mask_float.astype(np.float32))*self.eff_defocus_OTF))        
        if self.clear_board_toggle:
            defocused_projected_mask = defocused_projected_mask[:,self.board_crop_px:-self.board_crop_px]
            assert defocused_projected_mask.shape[1] == self.W_crop, "clear board operation error!"
        self.defocused_projected_mask_uint = np.clip(defocused_projected_mask, 0, 255).astype(np.uint8)

    def resize_result(self):
        # TODO : 
        '''    
        from skimage.measure import block_reduce
        # version 2: block_reduce (pixel binning)
        if self.resize_factor * self.resize_factor_along_width != 1.0:
            resized_result = block_reduce(self.projected_mask_uint, (self.resize_factor, self.resize_factor_along_width), np.mean)
            resized_defocused_result = block_reduce(self.defocused_projected_mask_uint, (self.resize_factor, self.resize_factor_along_width), np.mean)
        else:
            resized_result = self.projected_mask_uint
            resized_defocused_result = self.defocused_projected_mask_uint

        '''
        # version 1: cv2.resize
        if self.resize_factor * self.resize_factor_along_width != 1.0:
            resized_result = cv2.resize(self.projected_mask_uint, 
                                        (int(self.resized_W), int(self.resized_H)), 
                                        interpolation=cv2.INTER_AREA)
            resized_defocused_result = cv2.resize(self.defocused_projected_mask_uint, 
                                                  (int(self.resized_W), int(self.resized_H)), 
                                                  interpolation=cv2.INTER_AREA)
        else:
            resized_result = self.projected_mask_uint
            resized_defocused_result = self.defocused_projected_mask_uint
        
        self.resized_result_uint = resized_result            
        self.resized_defocused_result_uint = resized_defocused_result

    def save_image(self, path=None, output_dir=None):
        if path is None:
            path = self.header_prefix + 'projected_image.bmp'
        if output_dir:
            import os
            path = os.path.join(output_dir, os.path.basename(path))
        cv2.imwrite(f'{path}', self.resized_result_uint)
        print(f"Resized result image saved to {path}")
        cv2.imwrite(f'{path.replace("projected_image.bmp", "defocused_projected_image.bmp")}', self.resized_defocused_result_uint)
        print(f"Resized defocused result image saved to {path.replace('projected_image.bmp', 'defocused_projected_image.bmp')}")



    def plot_matplotlib_image_crs(self):
        fig, ax = plt.subplots(2, 2, figsize=(14, 9))

        um_v = self.resized_sampling_width_in_um
        um_h = self.resized_sampling_width_in_um_along_width

        v_profile = self.resized_defocused_result_uint[:, int((self.W_crop / self.resize_factor) // 2)]
        h_profile = self.resized_defocused_result_uint[int((self.H / self.resize_factor) // 2), :]

        # Row 1: cross-section
        for i, (profile, um_per_px, title, xlabel) in enumerate([
            (v_profile, um_v, "Projected Intensity Profile (vertical)", "Height"),
            (h_profile, um_h, "Projected Intensity Profile (horizontal)", "Width"),
        ]):
            mm_per_px = um_per_px / 1000
            px = np.arange(len(profile))
            ax[0, i].plot(px, profile)
            ax[0, i].set_ylim(0, 255)
            ax[0, i].set_title(title)
            ax[0, i].set_xlabel(f"{xlabel} (px)  [1 px = {um_per_px:.3f} um]")
            ax[0, i].set_ylabel("Gray (uint8)")
            ax[0, i].grid(True)
            sec = ax[0, i].secondary_xaxis('top',
                functions=(lambda x, s=mm_per_px: x * s, lambda x, s=mm_per_px: x / s))
            sec.set_xlabel("mm")

        # Row 2: FFT
        for i, (profile, um_per_px, title) in enumerate([
            (v_profile, um_v, "FFT (vertical)"),
            (h_profile, um_h, "FFT (horizontal)"),
        ]):
            n = len(profile)
            centered = profile.astype(np.float64) - np.mean(profile)
            fft_full = np.abs(np.fft.fft(centered))
            freqs_full = np.fft.fftfreq(n)

            pos_mask = freqs_full > 0
            freqs_pos = freqs_full[pos_mask]
            spectrum_pos = fft_full[pos_mask]

            peak_idx = np.argmax(spectrum_pos)
            peak_freq = freqs_pos[peak_idx]
            peak_mag = spectrum_pos[peak_idx]

            ax[1, i].plot(freqs_pos, spectrum_pos)
            ax[1, i].set_title(title)
            ax[1, i].set_xlabel("Spatial frequency (cycles/px)")
            ax[1, i].set_ylabel("Magnitude")
            ax[1, i].grid(True)
            ax[1, i].set_xlim(0, peak_freq * 6)

            if peak_freq > 0:
                period_px = 1.0 / peak_freq
                period_mm = period_px * um_per_px / 1000
                ax[1, i].annotate(
                    f"Period = {period_px:.1f} px ({period_mm:.4f} mm)",
                    xy=(peak_freq, peak_mag),
                    xytext=(0.55, 0.85), textcoords='axes fraction',
                    arrowprops=dict(arrowstyle='->', color='red'),
                    fontsize=9, color='red', fontweight='bold',
                )

        fig.tight_layout()
        return fig

      
    
    def psf_prop(self, progress_callback=None):
        z_step = 64
        self.z_list = np.linspace(-self.DOF_bidirec_mm, self.DOF_bidirec_mm, z_step)
        psfs = []
        self.defocus_z1_mm = 0
        self.initialize_optics()
        for i, z_mm in enumerate(self.z_list):
            if progress_callback:
                progress_callback(i, z_step, f"PSF propagation: z={z_mm:.3f} mm ({i+1}/{z_step})")
            # calculate OTF with "defocused OTF" within onfocus grid 
            self.calculate_OTF(user_z1_defo_mm=z_mm, disable_tqdm=True)
            
            # scale the defocused PSF from the onfocus grid to defocused grid
            scale = (self.z1_mm+z_mm)/(self.z1_mm+0)
            resized = affine_scale_image_with_warp(self.eff_defo_psf, scale)
            
            psfs.append(resized)
            
        psfs = np.array(psfs)
        # Plot a central slice along the smaller spatial dimension
        if self.W > self.H:
            # Width is smaller: slice along the third axis (depth) at center of width
            slice_index = int(self.W / 2) + 1
            psf_crs = psfs[:, int(self.H/2-z_step*2):int(self.H/2+z_step*2), slice_index]
        else:
            # Height is smaller or equal: slice along the second axis (height) at center of height
            slice_index = int(self.H / 2) + 1
            psf_crs = psfs[:, slice_index, int(self.W/2-z_step*2):int(self.W/2+z_step*2)]
        
        
        self.psf_crs_uint = (psf_crs/np.max(psf_crs)*255).astype(np.uint8)

    def plot_matplotlib_psf_crs(self):
        fig, ax = plt.subplots(figsize=(12, 6), dpi=400)        
        z_axis = self.z_list+self.z1_mm
        _W = self.psf_crs_uint.shape[1]
        ax.plot(z_axis, self.psf_crs_uint[:,_W//2])
        ax.set_ylim(0, 255)
        ax.set_title("PSF Intensity Profile (along optical axis)")
        ax.set_xlabel("Axial position [mm]")
        ax.set_ylabel("Gray (uint8)")
        ax.grid(True)
        return fig
    
    def run(self, bmp_path, json_path, parameters=None):
        self.load_image(bmp_path)
        self.load_grating_parameters(json_path)
        if parameters is not None:
            self.update_parameters()    
        self.initialize_optics()
        self.check_simulation_condition()
        self.calculate_OTF()
        self.perform_OTF()
        self.resize_result()
        self.save_image()
        self.plot_matplotlib_image_crs()
        self.psf_prop()
        self.plot_matplotlib_psf_crs()
    
    def check_psf_prop(self, progress_callback=None):
        self.initialize_optics()
        self.check_simulation_condition()
        self.psf_prop(progress_callback=progress_callback)
     
        
def affine_scale_image_with_warp(img, scale, maintain_size=True):
    """
    Scale an image by `scale` using cv2.warpAffine.
    
    If maintain_size=True, the output will be the same shape as the input and
    the scaling will be centered.  If False, the output size will be scaled
    by `scale` (no padding/cropping).
    """
    H, W = img.shape[:2]
    # center of the image
    cx, cy = W / 2.0, H / 2.0

    # get a 2×3 affine transform for scaling about the center
    M = cv2.getRotationMatrix2D((cx, cy), angle=0, scale=scale)

    if maintain_size:
        # output the same (W,H)
        dsize = (W, H)
        out = cv2.warpAffine(
            img, M, dsize,
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=0
        )
    else:
        # output a new size = (scaled_W, scaled_H)
        newW = int(round(W * scale))
        newH = int(round(H * scale))
        # When resizing without preserving size, you generally want
        # to drop the translation part so that the top-left of the
        # scaled image aligns to (0,0).  You can zero out M[:,2]:
        M_nopad = M.copy()
        M_nopad[0, 2] = 0
        M_nopad[1, 2] = 0
        out = cv2.warpAffine(
            img, M_nopad, (newW, newH),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=0
        )
    return out

if __name__ == '__main__':
    
    
    pis = Projection_image_simulator()    
    pis.pupil_diameter_mm = pis.z1_mm*0.005*2
    pis.defocus_z1_mm = 20
    # pis.clear_board_toggle = False
    pis.run('test_grating_close(True).bmp', 'test_params.json')
    print(f'NA: {pis.img_space_na:.4f}')
    plt.figure()
    plt.imshow(pis.eff_defocus_OTF_uint)
    plt.show()
    plt.figure()
    plt.imshow(pis.eff_defo_psf)
    plt.show()
    plt.imshow(pis.resized_result_uint)
    plt.plot(pis.resized_result_uint[150,:])
    plt.plot(pis.resized_result_uint[:,150])
    
    # DOF_bidirec_mm = 1e-3*pis.wvls_um[0]/pis.img_space_na**2
    # print(f'DOF: {DOF_bidirec_mm:.2f} mm')
    
    # pis.check_psf_prop()
    # plt.imshow(pis.eff_Phi_angle_uint)
    # plt.show()
    # plt.imshow(pis.psf_crs_uint[:,:])
    # plt.show()
    # plt.plot(pis.psf_crs_uint[:,128])
    # plt.show()
    
    #%%


    
