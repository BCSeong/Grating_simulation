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

    def analyze_sine_direction(self):
        f_transform = np.fft.fft2(self.img)
        f_shift = np.fft.fftshift(f_transform)
        magnitude_spectrum = np.abs(f_shift)

        rows, cols = self.img.shape
        cy, cx = rows // 2, cols // 2

        y, x = np.indices((rows, cols))
        angles = np.arctan2(y - cy, x - cx)
        radius = np.hypot(x - cx, y - cy)

        min_radius = 10
        max_radius = min(rows, cols) // 4
        mask = (radius > min_radius) & (radius < max_radius)

        angle_hist, bins = np.histogram(
            angles[mask], bins=180,
            weights=magnitude_spectrum[mask], range=(-np.pi, np.pi))

        max_idx = np.argmax(angle_hist)

        window_size = 2
        idx_range = range(max(0, max_idx - window_size),
                          min(len(angle_hist), max_idx + window_size + 1))
        x_points = np.array([bins[i] + (bins[i+1] - bins[i]) / 2 for i in idx_range])
        y_points = np.array([angle_hist[i] for i in idx_range])

        if len(x_points) >= 3:
            coeffs = np.polyfit(x_points, y_points, 2)
            a, b, c = coeffs
            if a < 0:
                refined_angle = -b / (2 * a)
                self.detected_angle_deg = np.degrees(refined_angle)
            else:
                dominant_angle = (bins[max_idx] + bins[max_idx + 1]) / 2
                self.detected_angle_deg = np.degrees(dominant_angle)
        else:
            dominant_angle = (bins[max_idx] + bins[max_idx + 1]) / 2
            self.detected_angle_deg = np.degrees(dominant_angle)

        self._magnitude_spectrum = magnitude_spectrum
        self._angle_hist = angle_hist
        self._angle_bins = bins

        return self.detected_angle_deg

    def rotate_and_extract(self, angle_deg=None):
        if angle_deg is not None:
            self.user_angle_deg = angle_deg
            use_angle = angle_deg
        else:
            use_angle = self.detected_angle_deg

        rotation_angle = 90 + use_angle
        h, w = self.img.shape[:2]
        M = cv2.getRotationMatrix2D((w / 2, h / 2), rotation_angle, 1.0)
        cos_a = abs(M[0, 0])
        sin_a = abs(M[0, 1])
        new_w = int(h * sin_a + w * cos_a)
        new_h = int(h * cos_a + w * sin_a)
        M[0, 2] += (new_w - w) / 2
        M[1, 2] += (new_h - h) / 2
        self.rotated_img = cv2.warpAffine(self.img, M, (new_w, new_h))

        center_col = self.rotated_img.shape[1] // 2
        self.cross_section_profile = self.rotated_img[:, center_col].astype(np.float64)

        centered = self.cross_section_profile - np.mean(self.cross_section_profile)
        fft_full = np.abs(np.fft.fft(centered))
        freqs_full = np.fft.fftfreq(len(centered))

        pos_mask = freqs_full > 0
        self.fft_freqs = freqs_full[pos_mask]
        self.fft_magnitude = fft_full[pos_mask]

        if len(self.fft_magnitude) > 0:
            peak_idx = np.argmax(self.fft_magnitude)
            self.peak_freq = self.fft_freqs[peak_idx]
            self.peak_period_px = 1.0 / self.peak_freq if self.peak_freq > 0 else 0

    def plot_analysis(self, pixel_size_um=None):
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        axes[0, 0].imshow(self.img, cmap='gray')
        axes[0, 0].set_title('Original Image')

        axes[0, 1].imshow(self.rotated_img, cmap='gray')
        center_col = self.rotated_img.shape[1] // 2
        axes[0, 1].axvline(x=center_col, color='r', linewidth=0.5, alpha=0.7)
        angle_used = self.user_angle_deg if self.user_angle_deg is not None else self.detected_angle_deg
        axes[0, 1].set_title(f'Rotated (angle={angle_used:.2f} deg)')

        ax_profile = axes[1, 0]
        px = np.arange(len(self.cross_section_profile))
        ax_profile.plot(px, self.cross_section_profile)
        ax_profile.set_ylim(0, 255)
        ax_profile.set_xlabel('Pixel Position')
        ax_profile.set_ylabel('Intensity')
        ax_profile.set_title('Cross-Section Profile')
        ax_profile.grid(True)

        if pixel_size_um is not None and pixel_size_um > 0:
            mm_per_px = pixel_size_um / 1000
            sec = ax_profile.secondary_xaxis('top',
                functions=(lambda x: x * mm_per_px, lambda x: x / mm_per_px))
            sec.set_xlabel("mm")

        ax_fft = axes[1, 1]
        ax_fft.plot(self.fft_freqs, self.fft_magnitude)
        ax_fft.set_xlabel('Spatial frequency (cycles/px)')
        ax_fft.set_title('FFT Spectrum')
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
