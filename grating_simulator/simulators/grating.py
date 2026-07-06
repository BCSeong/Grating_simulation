import numpy as np
import matplotlib.pyplot as plt
import cv2




class Grating_generator():
    def __init__(self):
        # general parameters
        self.gt_id = '21um_EPI' # str, headerLineEdit
        self.mask_sampling_width_in_um = 0.05 # float, samplingPixelSizeUmDoubleSpinBox
        # advanced parameters
        self.diameter_of_edge_of_saw_in_um = .4 # float, diameterOfEdgeOfSawtoothUmDoubleSpinBox
        self.mask_rounding = True # True False, methodComboBox
        self.round_size_px = 'AUTO' # 'AUTO', None, 'User', methodComboBox
        self.round_size_px_user = 1 # int, factorSpinBox

        # grating parameters
        self.period_pattern = 20.8 # float, periodOfPatternUmDoubleSpinBox
        self.amplitude_of_saw = 5.2 # float, heightOfSawtoothUmDoubleSpinBox
        self.period_of_saw = 1.98 # float, periodOfSawtoothUmDoubleSpinBox
        self.width_of_stem = 3.78 # float, widthOfStemUmDoubleSpinBox
        self.offset_btw_pattern = 6.62 # float, offsetBtwLinesDoubleSpinBox

        self.number_of_pattern = 3 # int, numOfLinesSpinBox
        self.length_of_grating_in_um = 20 # float, lengthOfLineUmDoubleSpinBox
        
        self.invert_result = False
        
    
    def init(self, parameters):
        for key, value in parameters.items():
            setattr(self, key, value)
        

    def generate_grating(self):
        """
        ASCII 도식 - 이등변 삼각형을 반으로 자른 직각삼각형 (C 선분 포함, 1/3 지점)

        ▲ y축 방향 (위로)
        |
        |         /|
        |        / |
        |       /  |
        |      /   |
        |     /----|   ← 선분 C (길이 c/2) : Grating 패턴 꼭지점의 너비
        |    /     |
        |   /      |
        |  /       | a ← B와 C 중심 간 거리
        | /        |
        |/---------|   ← 선분 B (길이 b/2) : Grating 삼각형 밑면의 너비
            
        이등변 삼각형의 전체 높이 h 계산:
            h = (a * b) / (b - c)
        """
        a = self.amplitude_of_saw-self.diameter_of_edge_of_saw_in_um/2
        b = self.period_of_saw
        c = self.diameter_of_edge_of_saw_in_um
        # grating parameters ----------------------------------------------------------
        A = a*b/(b-c)
        B1 = self.width_of_stem/2  
        B2 = -(A + B1)  # Offset for f2 in micrometers
        T = self.period_of_saw  # Period in micrometers
        dx = self.mask_sampling_width_in_um  # mask Sampling interval in micrometers
        # -----------------------------------------------------------------------------

        pad =  self.period_gen_sine-(A+B1-B2)

        # Generate x and y ranges for the 2D array
        y = np.arange(B2-pad, B1+A, dx)
        x = np.arange(-self.length_of_grating_in_um/2, self.length_of_grating_in_um, dx)

        # Create the 2D grid
        X, Y = np.meshgrid(x, y)

        # Define triangle trains
        f1 = A * np.abs(2 * ((X / T) - np.floor((X / T) + 0.5))) + B1
        f2 = A * np.abs(2 * ((X / T) - np.floor((X/ T) + 0.5))) + B2

        # Create mask: area between f1 and f2 is 0, elsewhere is 1
        mask = np.where((Y >= f2) & (Y <= f1), 0, 1)
        self.mask_ori = ~np.array(mask, dtype=bool)



        if self.mask_rounding:    

            def mask_edge_rounder(mask, kernel_size, target_period):
                if not kernel_size == 0:
                    structuring_element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
                    closed_mask = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_CLOSE, structuring_element)
                    _mask = closed_mask[:,kernel_size:-kernel_size] 
                    mask_rev = np.array(_mask, dtype=bool)
                    mask_rev = ~mask_rev
                else:
                    mask_rev = np.array(mask, dtype=bool)
                    mask_rev = ~mask_rev

                # 각 행(row)마다 True 값이 하나라도 있는 행들의 인덱스를 찾기
                row_indices = np.where(np.any(mask_rev, axis=1))[0]

                # 평가
                min_ind = row_indices[0]           # 첫 True가 있는 행 (top)
                max_ind = row_indices[-1]          # 마지막 True가 있는 행 (bottom)
                height = max_ind - min_ind + 1     # 최종 패턴의 높이
                period_est = len(mask)-height      # 다음 패턴과의 주기

                est_result = [height, period_est]
                crit = height*dx - target_period
                
                return mask_rev, crit, est_result
        

            
            if self.round_size_px is None:
                kernel_size = 0
            elif self.round_size_px == 'AUTO':
                kernel_size = int((A-a)/dx/3)
            else:
                kernel_size = self.round_size_px_user
                
            target_period = self.amplitude_of_saw*2+self.width_of_stem
            
            
            mask_rev, crit, est_result = mask_edge_rounder(mask, kernel_size, target_period)
            

            if self.round_size_px == 'AUTO':        
                print("Performing AUTO rounding ... \n\t Goal: The generated and measured patterns must have the same period.")        
                if crit > dx*2:                
                    print("\t\t -> dist:", end = '')
                    while np.abs(crit)> dx*5:
                        kernel_size+=1
                        mask_rev, crit, est_result = mask_edge_rounder(mask, kernel_size, target_period)                
                        print(f"{crit:.1f}, ", end='')

                if crit < dx*2:    
                    print("\t\t -> dist:", end = '')
                    while np.abs(crit)> dx*5:
                        kernel_size-=1
                        mask_rev, crit, est_result = mask_edge_rounder(mask, kernel_size, target_period)    
                        print(f"{crit:.1f}, ", end='')

            
            print("\n\t\t\t -> done !!\n\n")

            print('---------------------------------------------------------------------')
            print(f'Generated pattern width = {est_result[0]*dx} um')
            print(f'Measured pattern width = {self.amplitude_of_saw*2+self.width_of_stem} um')
            print()    
            print(f'Generated offest btw patterns= {est_result[1]*dx} um')
            print(f'Measured offest btw patterns= {self.offset_btw_pattern} um')
            print()
            print(f'Generated Period of patterns= {len(mask)*dx} um')
            print(f'Measured Period of patterns= {self.period_pattern} um')
            print()
            self.mask_gen = mask_rev

        else:
            self.mask_gen = mask


    def check_parameter_consistency(self):
        # check1: Input parameter consistency checks.
        self.period_gen_sine = (self.amplitude_of_saw+self.width_of_stem/2 +self.offset_btw_pattern/2)*2
        consistency_check = self.period_gen_sine-self.period_pattern<1e-4 # print pass of fail on, parameterConsistencyCheckLineEdit and terminal
        print('---------------------------------------------------------------------')
        print(f'Calcurated period of pattern in sine wave direction : {self.period_gen_sine} um')
        print(f'Measured period of pattern in sine wave direction : {self.period_pattern} um')
        print(f'\tParameter Consistency Check: {"Pass" if consistency_check else "Fail"}')
        print()
        assert consistency_check, "!!Input parameter error: The measured and calculated pattern periods are different!"

    def image_stacker(self):
        buffer = self.mask_gen.copy()
        if self.number_of_pattern >1:
            for _ in range(self.number_of_pattern-1):
                buffer = np.vstack((buffer,self.mask_gen))
        self.buffer = buffer
        self.H = buffer.shape[0]
        self.W = buffer.shape[1]
    
    def matplot_grating(self):
        # Plot the mask on groupBox_5
        plt.figure()
        plt.imshow(self.mask_ori, cmap="gray")
        plt.colorbar(label="Mask Value")
        plt.title("2D Mask Generated from Triangle Trains")
        plt.xlabel("x (px)")
        plt.ylabel("y (px)")
        plt.axis('image')
        plt.grid(False)
        plt.show()
        # Plot the mask on groupBox_6
        plt.figure()
        plt.imshow(self.mask_gen, cmap="gray")
        plt.colorbar(label="Mask Value")
        plt.title("2D Mask Generated from Triangle Trains with Rounding")
        plt.xlabel("x (px)")
        plt.ylabel("y (px)")
        plt.axis('image')
        plt.grid(False)
        plt.show()
        # Plot the mask on groupBox_7
        plt.figure()
        plt.imshow(self.buffer, cmap="gray")
        plt.colorbar(label="Mask Value")
        plt.title("2D Mask Generated from Triangle Trains with Rounding")
        plt.xlabel("x (px)")
        plt.ylabel("y (px)")
        plt.axis('image')
        plt.grid(False)
        plt.show()

    def save_grating(self, output_dir=None):
        import os
        filename = f'{self.gt_id}grating_close({self.mask_rounding}).bmp'
        filename_rev = f'{self.gt_id}grating_close({self.mask_rounding})_rev.bmp'
        if output_dir:
            filename = os.path.join(output_dir, filename)
            filename_rev = os.path.join(output_dir, filename_rev)
        cv2.imwrite(filename, self.buffer*255)
        cv2.imwrite(filename_rev, ~self.buffer*255)
        print(f"Grating saved to {filename}")
    
    def invert_grating(self):
        self.mask_ori = ~self.mask_ori
        self.mask_gen = ~self.mask_gen
        self.buffer = ~self.buffer

    def run(self, display=False, save=False):
        self.check_parameter_consistency()
        self.generate_grating()        
        self.image_stacker()

        if self.invert_result:
            self.invert_grating()
        if display:
            self.matplot_grating()
        if save:
            self.save_grating()
        



if __name__ == '__main__':

    GG = Grating_generator()
    GG.run()

    print(GG.mask_gen.dtype)
    print(GG.mask_ori.dtype)
    print(GG.buffer.dtype)

    GG2 = Grating_generator()
    params = {'invert_result':True}
    GG2.init(params)
    GG2.run(display=True)


