# 프로젝트 아키텍처

## 개요

Grating Simulator는 회절격자(grating) 패턴 생성부터 현미경/프로젝션 광학 시뮬레이션, Scheimpflug 보정, FFT 이미지 분석까지 수행하는 PySide6 기반 GUI 애플리케이션입니다.

## 디렉토리 구조

```
atp2_20250424_refactoring_GUIver/
├── run.py                          # 진입점 (Entry point)
├── run.bat                         # Windows 실행 스크립트
├── install.bat                     # 가상환경 생성 + 의존성 설치
├── requirements.txt                # Python 패키지 의존성
│
├── grating_simulator/              # 메인 패키지
│   ├── __init__.py
│   ├── app.py                      # MainWindow (GUI 전체 로직)
│   │
│   ├── ui/                         # UI 관련
│   │   ├── main_window.ui          # Qt Designer 원본 UI
│   │   ├── main_window_ui.py       # uic 자동생성 코드 (수정 금지)
│   │   └── widgets.py              # 커스텀 위젯 (ZoomableGraphicsView, PopupWindow 등)
│   │
│   └── simulators/                 # 시뮬레이션 엔진
│       ├── grating.py              # 격자 패턴 생성기
│       ├── microscope.py           # 현미경 이미지 시뮬레이터 (OTF 기반)
│       ├── projection.py           # 프로젝션 이미지 시뮬레이터 (OTF + defocus)
│       ├── scheimpflug.py          # Scheimpflug 보정 시뮬레이터 (homography)
│       └── fft_analyzer.py         # FFT 이미지 분석기
│
├── bin/                            # 레거시 독립 실행 스크립트 (참고용)
│   ├── 20M20um/                    # 실험 데이터 분석 스크립트
│   └── *.py                        # 이전 버전 스크립트
│
├── output/                         # 세션별 출력 폴더 (YYYYMMDD_HHMMSS/)
└── docs/                           # 문서
```

## 탭 구성

| 탭 | 이름 | 시뮬레이터 클래스 | 설명 |
|---|---|---|---|
| Tab 1 | Grating Generator | `Grating_generator` | 이진 격자 마스크 생성 |
| Tab 2 | Microscope Simulator | `Microscope_image_simulator` | OTF 기반 현미경 이미징 시뮬레이션 |
| Tab 3 | Scheimpflug Simulator | `Scheimpflug_simulator` | Scheimpflug 조건 하의 homography 보정 |
| Tab 4 | Projection Simulator | `Projection_image_simulator` | 프로젝션 이미징 + defocus OTF 시뮬레이션 |
| Tab 5 | FFT Image Analysis | `FFTImageAnalyzer` | 사인파 방향 감지 + 주기 측정 |

## 핵심 설계 원칙

### 1. 시뮬레이터 ↔ GUI 분리
각 시뮬레이터 클래스(`simulators/`)는 GUI 독립적으로 동작합니다. `app.py`의 `MainWindow`가 이들을 인스턴스화하고 UI 이벤트와 연결합니다.

### 2. 세션 기반 출력
매 실행마다 `output/YYYYMMDD_HHMMSS/` 폴더가 생성되어, 모든 결과 이미지와 파라미터 JSON이 해당 세션 폴더에 저장됩니다.

### 3. 선택적 GPU 가속
`scheimpflug.py`의 거리/감쇠 맵 계산은 torch(CUDA)와 numpy(CPU) 두 가지 백엔드를 지원합니다. torch가 설치되지 않으면 자동으로 numpy로 fallback됩니다.

### 4. 최소 의존성
필수: PySide6, numpy, opencv-python, matplotlib, tqdm
선택: torch (GPU 가속용)

## 데이터 흐름

```
[Tab 1] 격자 생성 → BMP 저장
            ↓
[Tab 2] 격자 BMP 로드 → OTF 적용 → 현미경 이미지 시뮬레이션
            ↓
[Tab 4] 격자 BMP 로드 → 프로젝션 OTF → defocus 시뮬레이션 → BMP 저장
            ↓
[Tab 3] 프로젝션 BMP 로드 → Scheimpflug homography → 밝기 감쇠 보정

[Tab 5] 임의 이미지 로드 → FFT 기반 사인파 분석 (독립)
```

## UI 위젯

| 위젯 | 파일 | 용도 |
|---|---|---|
| `ZoomableGraphicsView` | `widgets.py` | 마우스 휠 줌 지원 이미지 뷰어 |
| `PopupWindow` | `widgets.py` | matplotlib figure 팝업 표시 |
| `TextRedirector` | `widgets.py` | stdout/stderr → QTextEdit 리디렉션 |
