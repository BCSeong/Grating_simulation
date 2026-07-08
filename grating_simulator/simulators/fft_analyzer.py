import numpy as np
import cv2
import matplotlib.pyplot as plt


class FFTImageAnalyzer:
    def __init__(self):
        self.img = None
        self.H = 0
        self.W = 0
        self.detected_angle_deg = None
        self.user_angle_deg = None
        self.rotated_img = None
        self.cross_section_profile = None
        self.fft_magnitude = None
        self.fft_freqs = None
        self.peak_freq = None
        self.peak_period_px = None

    def load_image(self, file_path):
        self.img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if self.img is None:
            raise FileNotFoundError(f"Cannot load image: {file_path}")
        self.H, self.W = self.img.shape[:2]
        self.detected_angle_deg = None
        self.user_angle_deg = None
        self.rotated_img = None

    def analyze_sine_direction(self, progress_callback=None):
        if progress_callback:
            progress_callback(1, 3, "Preparing image...")

        rows, cols = self.img.shape
        crop_h, crop_w = rows // 2, cols // 2
        start_y = (rows - crop_h) // 2
        start_x = (cols - crop_w) // 2
        cropped = self.img[start_y:start_y + crop_h, start_x:start_x + crop_w].astype(np.float64)

        rows_c, cols_c = cropped.shape
        window = np.outer(np.hanning(rows_c), np.hanning(cols_c))
        cropped *= window

        if progress_callback:
            progress_callback(2, 3, "Computing 2D FFT...")

        f_transform = np.fft.fft2(cropped)
        f_shift = np.fft.fftshift(f_transform)
        magnitude = np.abs(f_shift)

        cy, cx = rows_c // 2, cols_c // 2

        y, x = np.ogrid[:rows_c, :cols_c]
        r = np.hypot(x - cx, y - cy)
        mag_masked = magnitude.copy()
        mag_masked[r < 3] = 0

        upper = mag_masked[:cy, :]
        peak_y, peak_x = np.unravel_index(np.argmax(upper), upper.shape)

        w = 5
        y_lo = max(0, peak_y - w)
        y_hi = min(upper.shape[0], peak_y + w + 1)
        x_lo = max(0, peak_x - w)
        x_hi = min(upper.shape[1], peak_x + w + 1)
        region = upper[y_lo:y_hi, x_lo:x_hi]
        yy, xx = np.meshgrid(np.arange(y_lo, y_hi), np.arange(x_lo, x_hi), indexing='ij')
        weight = region ** 2
        total = np.sum(weight)
        if total > 0:
            ref_y = np.sum(yy * weight) / total
            ref_x = np.sum(xx * weight) / total
        else:
            ref_y, ref_x = float(peak_y), float(peak_x)

        if progress_callback:
            progress_callback(3, 3, "Detecting angle...")

        alpha = np.degrees(np.arctan2(ref_y - cy, ref_x - cx))
        rotation = alpha + 90
        self.detected_angle_deg = ((rotation + 45) % 90) - 45

        self._magnitude_spectrum = magnitude

        return self.detected_angle_deg

    @staticmethod
    def _extract_1d_fft(profile):
        centered = profile - np.mean(profile)
        fft_full = np.abs(np.fft.fft(centered))
        freqs_full = np.fft.fftfreq(len(centered))
        pos_mask = freqs_full > 0
        freqs = freqs_full[pos_mask]
        magnitude = fft_full[pos_mask]
        peak_mag = np.max(magnitude) if len(magnitude) > 0 else 0
        return freqs, magnitude, peak_mag

    def rotate_and_extract(self, angle_deg=None, progress_callback=None):
        if angle_deg is not None:
            self.user_angle_deg = angle_deg
            use_angle = angle_deg
        else:
            use_angle = self.detected_angle_deg

        if progress_callback:
            progress_callback(1, 3, "Rotating image...")

        h, w = self.img.shape[:2]
        M = cv2.getRotationMatrix2D((w / 2, h / 2), use_angle, 1.0)
        cos_a = abs(M[0, 0])
        sin_a = abs(M[0, 1])
        new_w = int(h * sin_a + w * cos_a)
        new_h = int(h * cos_a + w * sin_a)
        M[0, 2] += (new_w - w) / 2
        M[1, 2] += (new_h - h) / 2
        self.rotated_img = cv2.warpAffine(self.img, M, (new_w, new_h))

        if progress_callback:
            progress_callback(2, 3, "Extracting profiles...")

        center_row = self.rotated_img.shape[0] // 2
        center_col = self.rotated_img.shape[1] // 2
        self.h_profile = self.rotated_img[center_row, :].astype(np.float64)
        self.v_profile = self.rotated_img[:, center_col].astype(np.float64)

        if progress_callback:
            progress_callback(3, 3, "Computing 1D FFT...")

        h_freqs, h_mag, h_peak = self._extract_1d_fft(self.h_profile)
        v_freqs, v_mag, v_peak = self._extract_1d_fft(self.v_profile)

        self.h_fft_freqs, self.h_fft_magnitude = h_freqs, h_mag
        self.v_fft_freqs, self.v_fft_magnitude = v_freqs, v_mag

        if h_peak >= v_peak:
            self.dominant_axis = 'H'
            self.cross_section_profile = self.h_profile
            self.fft_freqs, self.fft_magnitude = h_freqs, h_mag
        else:
            self.dominant_axis = 'V'
            self.cross_section_profile = self.v_profile
            self.fft_freqs, self.fft_magnitude = v_freqs, v_mag

        if len(self.fft_magnitude) > 0:
            peak_idx = np.argmax(self.fft_magnitude)
            self.peak_freq = self.fft_freqs[peak_idx]
            self.peak_period_px = 1.0 / self.peak_freq if self.peak_freq > 0 else 0

    def plot_analysis(self, pixel_size_um=None):
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        axes[0, 0].imshow(self.img, cmap='gray')
        axes[0, 0].set_title('Original Image')

        axes[0, 1].imshow(self.rotated_img, cmap='gray')
        center_row = self.rotated_img.shape[0] // 2
        center_col = self.rotated_img.shape[1] // 2
        axes[0, 1].axhline(y=center_row, color='b', linewidth=0.5, alpha=0.7)
        axes[0, 1].axvline(x=center_col, color='r', linewidth=0.5, alpha=0.7)
        angle_used = self.user_angle_deg if self.user_angle_deg is not None else self.detected_angle_deg
        axes[0, 1].set_title(f'Rotated (angle={angle_used:.2f} deg)')

        ax_profile = axes[1, 0]
        h_alpha = 1.0 if self.dominant_axis == 'H' else 0.3
        v_alpha = 1.0 if self.dominant_axis == 'V' else 0.3
        ax_profile.plot(np.arange(len(self.h_profile)), self.h_profile,
                        color='blue', alpha=h_alpha, label='Horizontal')
        ax_profile.plot(np.arange(len(self.v_profile)), self.v_profile,
                        color='red', alpha=v_alpha, label='Vertical')
        ax_profile.set_ylim(0, 255)
        ax_profile.set_xlabel('Pixel Position')
        ax_profile.set_ylabel('Intensity')
        ax_profile.set_title(f'Cross-Section Profile (dominant: {self.dominant_axis})')
        ax_profile.legend(fontsize=8)
        ax_profile.grid(True)

        if pixel_size_um is not None and pixel_size_um > 0:
            mm_per_px = pixel_size_um / 1000
            sec = ax_profile.secondary_xaxis('top',
                functions=(lambda x: x * mm_per_px, lambda x: x / mm_per_px))
            sec.set_xlabel("mm")

        ax_fft = axes[1, 1]
        ax_fft.plot(self.h_fft_freqs, self.h_fft_magnitude,
                    color='blue', alpha=h_alpha, label='Horizontal')
        ax_fft.plot(self.v_fft_freqs, self.v_fft_magnitude,
                    color='red', alpha=v_alpha, label='Vertical')
        ax_fft.set_xlabel('Spatial frequency (cycles/px)')
        ax_fft.set_title(f'FFT Spectrum (dominant: {self.dominant_axis})')
        ax_fft.legend(fontsize=8)
        ax_fft.grid(True)

        if self.peak_freq and self.peak_freq > 0:
            peak_idx = np.argmax(self.fft_magnitude)
            period_str = f"{self.peak_period_px:.1f} px"
            if pixel_size_um is not None and pixel_size_um > 0:
                period_um = self.peak_period_px * pixel_size_um
                period_str += f" ({period_um:.1f} um)"
            ax_fft.annotate(
                f'Peak: {self.peak_freq:.5f} cyc/px\nPeriod: {period_str}',
                xy=(self.peak_freq, self.fft_magnitude[peak_idx]),
                xytext=(self.peak_freq * 3, self.fft_magnitude[peak_idx] * 0.7),
                arrowprops=dict(arrowstyle='->', color='red'),
                fontsize=9, color='red')
            ax_fft.set_xlim(0, self.peak_freq * 6)

        fig.tight_layout()
        return fig
