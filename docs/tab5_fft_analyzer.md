# Tab 5: FFT Image Analysis (FFT 이미지 분석기)

**소스 파일**: `grating_simulator/simulators/fft_analyzer.py`

## 개요

임의의 사인파 패턴 이미지에서 주방향(dominant direction)과 공간 주기를 FFT 기반으로 자동 측정하는 범용 분석 도구입니다. 시뮬레이션 결과뿐만 아니라 실험 이미지에도 사용할 수 있습니다.

**의존성:** numpy, cv2, matplotlib (scipy 불필요)

---

## 클래스: `FFTImageAnalyzer`

### 생성자

```python
FFTImageAnalyzer()
```

모든 분석 결과 속성을 `None`/`0`으로 초기화합니다.

---

## 속성

### 입력 속성

| 속성 | 타입 | 초기값 | 설명 |
|---|---|---|---|
| `img` | `ndarray` or `None` | `None` | 로드된 그레이스케일 이미지 (uint8) |
| `H` | `int` | `0` | 이미지 높이 (px) |
| `W` | `int` | `0` | 이미지 너비 (px) |

### 분석 결과 속성

| 속성 | 타입 | 초기값 | 설정 시점 | 설명 |
|---|---|---|---|---|
| `detected_angle_deg` | `float` or `None` | `None` | `analyze_sine_direction()` | 자동 검출된 사인파 방향 각도 (도) |
| `user_angle_deg` | `float` or `None` | `None` | `rotate_and_extract()` | 사용자가 수동 지정한 각도 (도) |
| `rotated_img` | `ndarray` or `None` | `None` | `rotate_and_extract()` | 회전된 이미지 |
| `cross_section_profile` | `ndarray` or `None` | `None` | `rotate_and_extract()` | 중심 열의 강도 프로파일 (float64) |
| `fft_magnitude` | `ndarray` or `None` | `None` | `rotate_and_extract()` | 양의 주파수 영역 FFT magnitude |
| `fft_freqs` | `ndarray` or `None` | `None` | `rotate_and_extract()` | 양의 주파수 배열 (cycles/px) |
| `peak_freq` | `float` or `None` | `None` | `rotate_and_extract()` | FFT 피크 공간주파수 (cycles/px) |
| `peak_period_px` | `float` or `None` | `None` | `rotate_and_extract()` | 피크 주기 = `1/peak_freq` (px) |

### 내부 속성 (디버그/시각화용)

| 속성 | 타입 | 설명 |
|---|---|---|
| `_magnitude_spectrum` | `ndarray` | 2D FFT magnitude 스펙트럼 |
| `_angle_hist` | `ndarray` | 각도별 가중 히스토그램 (180 빈) |
| `_angle_bins` | `ndarray` | 히스토그램 빈 경계 (181개, -π ~ π) |

---

## 메서드

### `load_image(file_path)`

그레이스케일 이미지를 로드하고 분석 상태를 초기화합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `file_path` | `str` | 이미지 파일 경로 (BMP, PNG, TIFF 등 cv2 지원 형식) |

**반환값:** 없음

**예외:** 파일을 로드할 수 없으면 `FileNotFoundError`

**설정되는 속성:** `img` (uint8 그레이스케일), `H`, `W`

**초기화되는 속성:** `detected_angle_deg`, `user_angle_deg`, `rotated_img` → `None`

---

### `analyze_sine_direction()`

2D FFT를 이용하여 사인파 패턴의 주방향 각도를 검출합니다.

**파라미터:** 없음

**반환값:**

| 타입 | 설명 |
|---|---|
| `float` | 검출된 각도 (도, -180 ~ +180). `detected_angle_deg`에도 저장 |

**사전 조건:** `load_image()` 호출 완료

**알고리즘:**

1. **2D FFT**: `fft2(img)` → `fftshift` → magnitude 스펙트럼

2. **방사형 마스크**: DC 주변 노이즈 제거
   ```
   min_radius = 10 px
   max_radius = min(H, W) / 4 px
   mask = (radius > min_radius) AND (radius < max_radius)
   ```

3. **가중 각도 히스토그램**: 
   ```
   각 주파수 성분의 각도: θ = atan2(y - cy, x - cx)
   히스토그램: 180 빈, [-π, π] 범위
   가중치: magnitude 스펙트럼 값
   ```

4. **피크 검출**: 히스토그램 최대 빈

5. **Parabolic fitting (sub-bin 정밀도)**:
   ```
   피크 주변 ±2 빈의 점들에 2차 다항식 피팅
   y = ax² + bx + c
   a < 0 이면 (볼록):
       refined_angle = -b / (2a)
   그렇지 않으면:
       빈 중심값 사용
   ```

**설정되는 속성:** `detected_angle_deg`, `_magnitude_spectrum`, `_angle_hist`, `_angle_bins`

**정밀도:** parabolic fitting에 의해 빈 간격(2°) 이하의 각도 분해능 달성

---

### `rotate_and_extract(angle_deg=None)`

이미지를 지정된 각도로 회전시켜 패턴이 수직이 되도록 정렬한 후, 중심 열의 교차 단면을 추출하고 1D FFT로 공간 주기를 측정합니다.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `angle_deg` | `float` or `None` | `None` | 사용할 각도 (도). `None`이면 `detected_angle_deg` 사용. 지정 시 `user_angle_deg`에 저장 |

**반환값:** 없음

**사전 조건:** `load_image()` 호출 완료. `angle_deg=None`이면 `analyze_sine_direction()` 호출 완료

**알고리즘:**

1. **회전 각도 결정**: `rotation_angle = 90 + use_angle`
   - 사인파 방향이 수평이 되도록 90° 추가

2. **Bounding box 확장 회전**:
   ```python
   M = cv2.getRotationMatrix2D((w/2, h/2), rotation_angle, 1.0)
   cos_a = |M[0,0]|
   sin_a = |M[0,1]|
   new_w = int(h × sin_a + w × cos_a)
   new_h = int(h × cos_a + w × sin_a)
   M[0,2] += (new_w - w) / 2    # 중심 보정
   M[1,2] += (new_h - h) / 2
   rotated = cv2.warpAffine(img, M, (new_w, new_h))
   ```
   - 일반 회전과 달리 bounding box를 확장하여 이미지가 잘리지 않음
   - scipy 대신 cv2.warpAffine 사용 (scipy 의존성 제거)

3. **교차 단면 추출**: 회전 이미지의 중앙 열 (세로 프로파일)
   ```
   center_col = rotated.shape[1] // 2
   profile = rotated[:, center_col]    (float64 변환)
   ```

4. **1D FFT 분석**:
   ```
   centered = profile - mean(profile)     ← DC 제거
   fft_full = |FFT(centered)|
   freqs = fftfreq(len(centered))
   ```
   양의 주파수만 추출 → 피크 검출

5. **피크 주기 계산**:
   ```
   peak_idx = argmax(fft_magnitude[positive_freqs])
   peak_freq = freqs[peak_idx]           [cycles/px]
   peak_period = 1 / peak_freq           [px]
   ```

**설정되는 속성:** `user_angle_deg` (angle_deg 지정 시), `rotated_img`, `cross_section_profile`, `fft_magnitude`, `fft_freqs`, `peak_freq`, `peak_period_px`

---

### `plot_analysis(pixel_size_um=None)`

분석 결과를 2×2 figure로 시각화합니다.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `pixel_size_um` | `float` or `None` | `None` | 픽셀 크기 (μm/px). 지정 시 교차 단면에 mm 단위 보조 축 추가 |

**반환값:**

| 타입 | 설명 |
|---|---|
| `matplotlib.Figure` | 2×2 분석 figure |

**사전 조건:** `analyze_sine_direction()` + `rotate_and_extract()` 호출 완료

**Figure 구성:**

| 위치 | 내용 | 설명 |
|---|---|---|
| `[0,0]` | Original Image | 원본 이미지 (grayscale) |
| `[0,1]` | Rotated Image | 회전된 이미지 + 중앙 열 빨간 라인. 타이틀에 사용된 각도 표시 |
| `[1,0]` | Cross-Section Profile | 중심 열 강도 프로파일 (0-255). `pixel_size_um` 지정 시 상단에 mm 축 |
| `[1,1]` | FFT Spectrum | 공간주파수 스펙트럼 + 피크 주석 |

**피크 주석 형식:**
```
Peak: {peak_freq:.5f} cyc/px
Period: {period_px:.1f} px ({period_um:.1f} um)    ← pixel_size_um 지정 시
```

**x축 범위**: FFT 스펙트럼은 `peak_freq × 6`까지 표시 (고조파 확인 가능)

---

## GUI 조작 순서

1. **1. Load Image** → 분석할 이미지 선택 (BMP, PNG, TIFF 등)
2. **2. Auto-Detect Angle** → 2D FFT로 사인파 방향 자동 검출, Detected angle 필드에 표시
3. (선택) Manual angle 값 수정 → 자동 검출 결과 대신 사용자 지정 각도 사용
4. **3. Analyze & Plot** → 이미지 회전 + 1D FFT 분석 + 팝업 figure 표시
5. **4. Save Figure** → 분석 figure를 세션 폴더에 PNG 저장

### GUI 파라미터 위젯

| 위젯 | 타입 | 범위 | 설명 |
|---|---|---|---|
| Detected angle | `QLineEdit` (readonly) | — | 자동 검출된 각도 (도). Auto-Detect 후 표시 |
| Manual angle | `QDoubleSpinBox` | -180 ~ 180 | 사용자 수동 지정 각도 (도). 비어있으면 detected 사용 |
| Pixel size (μm) | `QDoubleSpinBox` | ≥ 0 | mm 축 변환용. 기본값 20.0 |
| Image size | `QLineEdit` (readonly) | — | `H × W px` 형태 표시 |

---

## 사용 예시

### 프로그래밍 방식 (CLI)

```python
from grating_simulator.simulators.fft_analyzer import FFTImageAnalyzer

analyzer = FFTImageAnalyzer()
analyzer.load_image('projected_image.bmp')

# 1) 방향 자동 검출
angle = analyzer.analyze_sine_direction()
print(f"Detected angle: {angle:.2f} deg")

# 2) 회전 + 1D FFT 분석 (자동 검출 각도 사용)
analyzer.rotate_and_extract()
print(f"Period: {analyzer.peak_period_px:.1f} px")

# 3) 수동 각도로 분석
analyzer.rotate_and_extract(angle_deg=15.0)

# 4) 결과 시각화
fig = analyzer.plot_analysis(pixel_size_um=20.0)
fig.savefig('analysis.png', dpi=300)
```

---

## 알고리즘 상세

### 2D FFT 각도 검출의 원리

사인파 패턴은 주파수 도메인에서 두 개의 대칭 피크로 나타납니다 (양/음 주파수). 이 피크들의 위치가 패턴의 방향을 결정합니다.

```
공간 도메인: 사인파 (각도 θ, 주기 T)
    ↓ 2D FFT
주파수 도메인: 두 피크 at (±f·cos(θ), ±f·sin(θ)), f = 1/T
```

가중 각도 히스토그램은 모든 주파수 성분의 magnitude를 각도별로 합산하여 주방향을 찾습니다. 이는 여러 주파수 성분이 존재하는 복잡한 패턴에서도 동작합니다.

### Parabolic fitting

히스토그램 빈 간격 (2°)보다 높은 정밀도를 얻기 위해 피크 주변의 점들에 2차 다항식을 피팅합니다:

```
y = ax² + bx + c
피크 위치 = -b / (2a)    (a < 0, 즉 볼록한 포물선일 때만)
```

이 방법은 FFT 기반 주파수 추정에서 흔히 사용되는 parabolic interpolation과 동일한 원리입니다.

### cv2 기반 회전 (scipy-free)

`cv2.warpAffine`을 사용하여 bounding box를 확장하는 회전을 구현합니다. 일반적인 `cv2.warpAffine`은 출력 크기가 입력과 같아 모서리가 잘리지만, 출력 크기를 회전된 이미지의 전체 범위로 계산하고 이동 행렬을 보정하여 이를 방지합니다.
