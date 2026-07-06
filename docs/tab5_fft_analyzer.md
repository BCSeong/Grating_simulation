# Tab 5: FFT Image Analysis (FFT 이미지 분석기)

## 개요

임의의 사인파 패턴 이미지의 방향(각도)과 공간 주기를 FFT 기반으로 자동 측정합니다. 시뮬레이션 결과뿐만 아니라 실험 이미지에도 사용할 수 있는 범용 분석 도구입니다.

## 시뮬레이터 클래스

**파일**: `grating_simulator/simulators/fft_analyzer.py`
**클래스**: `FFTImageAnalyzer`

### 메서드

| 메서드 | 설명 |
|---|---|
| `load_image(file_path)` | 그레이스케일 이미지 로드 |
| `analyze_sine_direction()` | 2D FFT로 사인파 주방향 각도 검출 |
| `rotate_and_extract(angle_deg)` | 이미지 회전 + 중심 열 cross-section 추출 + 1D FFT 피크 분석 |
| `plot_analysis(pixel_size_um)` | 2×2 분석 figure 생성 |

### 핵심 수학

1. **방향 검출 (2D FFT)**
   - 2D FFT → magnitude spectrum
   - 각도별 가중 히스토그램 (magnitude 가중)
   - 피크 각도 주변 parabolic fitting으로 sub-bin 정밀도

2. **주기 측정 (1D FFT)**
   - 검출 각도로 이미지 회전 (패턴이 수직이 되도록)
   - 중심 열 cross-section 추출
   - 1D FFT → 피크 주파수 → 주기 (픽셀 단위)

### 출력

| 속성 | 설명 |
|---|---|
| `detected_angle_deg` | 자동 검출된 각도 (도) |
| `rotated_img` | 회전된 이미지 |
| `cross_section_profile` | 중심 열 강도 프로파일 |
| `peak_freq` | FFT 피크 공간주파수 (cycles/px) |
| `peak_period_px` | 피크 주기 (픽셀) |

## GUI 조작 순서

1. **1. Load Image** → 분석할 이미지 선택
2. **2. Auto-Detect Angle** → 2D FFT로 방향 자동 검출
3. (선택) Manual angle 값 수정
4. **3. Analyze & Plot** → 이미지 회전 + 1D FFT 분석 + 팝업 figure
5. **4. Save Figure** → figure를 세션 폴더에 저장

### GUI 파라미터

| 파라미터 | 설명 |
|---|---|
| Detected angle (readonly) | 자동 검출된 각도 |
| Manual angle | 사용자 수동 지정 각도 (-180~180) |
| Pixel size (μm) | mm 단위 축 변환용 |

## 의존성

- numpy, cv2, matplotlib만 사용 (scipy 불필요)
- cv2.warpAffine 기반 이미지 회전 (bounding box 확장 지원)
