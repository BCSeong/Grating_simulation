# Grating Simulator

회절격자(grating) 패턴 생성, 광학 시뮬레이션, Scheimpflug 보정, FFT 이미지 분석을 통합한 PySide6 기반 GUI 애플리케이션입니다.

## 주요 기능

| 탭 | 기능 | 상세 문서 |
|---|---|---|
| Tab 1 | **격자 생성기** — 이진 격자 마스크 생성 (톱니파 기반, morphological rounding) | [tab1_grating_generator.md](docs/tab1_grating_generator.md) |
| Tab 2 | **현미경 시뮬레이터** — OTF 기반 비간섭 이미징 시뮬레이션 (다색 지원) | [tab2_microscope_simulator.md](docs/tab2_microscope_simulator.md) |
| Tab 3 | **Scheimpflug 시뮬레이터** — Homography 변환 + 역제곱/cos⁴ 밝기 감쇠 보정 | [tab3_scheimpflug_simulator.md](docs/tab3_scheimpflug_simulator.md) |
| Tab 4 | **프로젝션 시뮬레이터** — 프로젝션 OTF + 근축 탈초점 + through-focus PSF 전파 | [tab4_projection_simulator.md](docs/tab4_projection_simulator.md) |
| Tab 5 | **FFT 이미지 분석** — 2D FFT 방향 검출 + 1D FFT 주기 측정 (parabolic fitting) | [tab5_fft_analyzer.md](docs/tab5_fft_analyzer.md) |

전체 아키텍처: [docs/architecture.md](docs/architecture.md)
커스텀 위젯: [docs/widgets.md](docs/widgets.md)

## 설치

### 요구사항

- Python 3.9 이상
- Windows 10/11

### 자동 설치

```bash
install.bat
```

가상환경 생성 → 의존성 설치 → PyTorch 설치 옵션 (CUDA 12.8 / CPU-only / 건너뛰기)을 안내합니다.

### 수동 설치

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# GPU 가속 사용 시 (선택)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
```

## 실행

```bash
run.bat
```

또는:

```bash
venv\Scripts\activate
python run.py
```

## 의존성

### 필수

| 패키지 | 용도 |
|---|---|
| PySide6 | Qt6 GUI 프레임워크 |
| numpy | 수치 계산, FFT |
| opencv-python | 이미지 I/O, warpPerspective, warpAffine |
| matplotlib | 시각화, cross-section plot |
| tqdm | 진행률 표시 |

### 선택

| 패키지 | 용도 |
|---|---|
| torch | GPU 가속 (Scheimpflug 거리/감쇠 맵). 미설치 시 numpy로 자동 fallback |

## 프로젝트 구조

```
├── run.py                    # 진입점
├── install.bat               # 설치 스크립트
├── run.bat                   # 실행 스크립트
├── requirements.txt          # 의존성 목록
│
├── grating_simulator/        # 메인 패키지
│   ├── app.py                # MainWindow (GUI 로직)
│   ├── ui/                   # UI 정의 + 커스텀 위젯
│   │   ├── main_window.ui    # Qt Designer 원본
│   │   ├── main_window_ui.py # 자동생성 코드 (수정 금지)
│   │   └── widgets.py        # ZoomableGraphicsView, PopupWindow, TextRedirector
│   └── simulators/           # 시뮬레이션 엔진 (GUI 독립)
│       ├── grating.py        # 격자 패턴 생성
│       ├── microscope.py     # 현미경 OTF 시뮬레이션
│       ├── projection.py     # 프로젝션 OTF + defocus 시뮬레이션
│       ├── scheimpflug.py    # Scheimpflug homography + 밝기 감쇠
│       └── fft_analyzer.py   # FFT 방향/주기 분석
│
├── docs/                     # 문서 (OpenCV 스타일 API 레퍼런스)
├── bin/                      # 레거시 스크립트 (참고용)
└── output/                   # 세션별 결과 출력 (YYYYMMDD_HHMMSS/)
```

## 데이터 흐름

```
[Tab 1] 격자 생성 → BMP + JSON
            │
            ├──→ [Tab 2] 현미경 시뮬레이션
            │
            └──→ [Tab 4] 프로젝션 시뮬레이션 → BMP + JSON
                              │
                              └──→ [Tab 3] Scheimpflug 보정

[Tab 5] FFT 분석 ← 임의 이미지 (독립)
```

## CLI 사용

각 시뮬레이터는 GUI 없이 CLI에서 독립 실행할 수 있습니다:

```python
from grating_simulator.simulators.grating import Grating_generator
from grating_simulator.simulators.projection import Projection_image_simulator

# 격자 생성
gg = Grating_generator()
gg.run(save=True)

# 프로젝션 시뮬레이션
pis = Projection_image_simulator()
pis.pupil_diameter_mm = 3.0
pis.run('grating.bmp', 'grating_parameters.json')
```

## 출력

모든 결과는 `output/YYYYMMDD_HHMMSS/` 형식의 세션 폴더에 자동 저장됩니다. 실행 간 결과가 덮어씌워지지 않습니다.
