# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 21:47:09 2025

@author: Z4G5
"""

#%% Tab2
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

class Microscope_image_simulator():
    def __init__(self):
        self.NA:float = 0.0
        self.wvls:list = [0.5876]
        self.mask_sampling_width_in_um:float = 0.05
        self.H:int = 1 # image Height
        self.W:int = 1 # image Width
        self.mask_bmp = None # loaded image
        self.eff_OTF_uint = None # calcurated OTF
        self.imaged_gt_uint = None # result image
        
        self.set_parameters()

    def set_parameters(self):
        self.microscope_id = 'OTF_0.8NA_' # str, headerLineEdit
        self.NA = 0.8
        self.custom_spectrum = False
        self.custom_image_property = False        
        self.wvls = [0.5876]
        self.mask_sampling_width_in_um = 0.05        
        
        
    def load_image(self, path):
        self.mask_bmp = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        self.mask_bmp = self.mask_bmp.astype(np.float32)        
        self.H = self.mask_bmp.shape[0]
        self.W = self.mask_bmp.shape[1]        
        
    def load_grating_parameters(self, path):
        with open(path, 'r') as f:
            params = json.load(f)
        self.mask_sampling_width_in_um = params['mask_sampling_width_in_um']


    def initialize_optics(self):        
        self.dky = 1/(self.H*self.mask_sampling_width_in_um)
        self.dkx = 1/(self.W*self.mask_sampling_width_in_um)
        ky = np.arange(0, self.H*self.dky-self.dky/2, self.dky)
        ky -= np.max(ky)/2
        kx = np.arange(0, self.W*self.dkx-self.dkx/2, self.dkx)
        kx -= np.max(kx)/2        
        # Create the 2D grid    
        KX, KY = np.meshgrid(kx, ky)
        self.RHO = np.sqrt(KX**2+KY**2)

    def check_simulation_condition(self):
        min_cf = self.NA/np.min(self.wvls)
        check1 = min_cf < np.max(self.RHO)/5
        assert check1, 'NA is too large / sampling size of input image is too small'
        max_cf = self.NA/np.max(self.wvls)
        check2 = max_cf > min(self.dkx, self.dky)*4
        assert check2, 'NA is too small / sampling size of input image is too large'
        crit = check1 and check2 # pass of fail
        print('---------------------------------------------------------------------')
        print(f'* Cut off frequency, NA/lambda : {min_cf:.2f} um^-1 to {max_cf:.2f} um^-1')
        print(f'* Defiend Max Value in frequency domain, f_max : {np.max(self.RHO):.2f} um^-1')
        print(f'* Cut off frequency should be less than f_max/5 (Nyquist condition assuming OTF)')
        print(f'* Sampling size of frequency domain : {self.dkx:.2f} um^-1 (dkx), {self.dky:.2f} um^-1 (dky)')
        print(f'\t->Simulation Condition Check: {"Pass" if crit else "Fail"}')
        print()

    def calculate_OTF(self):
        OTFs=[]
        for lamb in tqdm(self.wvls, desc="Calcurating OTF "):
            cf = self.NA/lamb
            pupil = np.zeros_like(self.mask_bmp)
            pupil[self.RHO<=cf]=1
            psf = np.abs(myiFFT(pupil))**2
            OTF = myFFT(psf)
            OTFs.append(OTF)
        OTFs = np.array(OTFs)
        _eff_OTF = np.sum(OTFs, axis=0)
        _eff_OTF /= np.sum(_eff_OTF)
        self.eff_OTF = _eff_OTF
        self.eff_OTF_uint = (np.abs(self.eff_OTF) / np.max(np.abs(self.eff_OTF)) * 255).astype(np.uint8)
        

    def perform_OTF(self):
        imaged_gt = np.abs(myFFT(myiFFT(self.mask_bmp.astype(np.float32))*self.eff_OTF))
        self.imaged_gt_uint = (imaged_gt / np.max(imaged_gt) * 255).astype(np.uint8)

    def save_image(self, path=None, output_dir=None):
        if path is None:
            path = self.microscope_id + 'microscope_image.bmp'
        if output_dir:
            import os
            path = os.path.join(output_dir, os.path.basename(path))
        cv2.imwrite(path, self.imaged_gt_uint)
        print(f"Microscope image saved to {path}")


    def run(self, bmp_path, json_path):
        self.load_image(bmp_path)
        self.load_grating_parameters(json_path)
        self.set_parameters()
        self.initialize_optics()
        self.check_simulation_condition()
        self.calculate_OTF()
        self.perform_OTF()
        self.save_image()
    
    def get_OTF(self):
        return self.eff_OTF_uint
    def get_imaged_gt(self):
        return self.imaged_gt_uint

if __name__ == '__main__':
    mis = Microscope_image_simulator()

    mis.run('test_grating_close(True).bmp', 'test_params.json')
    
    plt.figure()
    plt.imshow(mis.eff_OTF_uint)
    plt.show()
    plt.figure()
    plt.imshow(mis.imaged_gt_uint)
    plt.show()
    
