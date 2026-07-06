# Grating Simulator

회절격자(grating) 패턴 생성, 광학 시뮬레이션, Scheimpflug 보정, FFT 이미지 분석을 통합한 PySide6 기반 GUI 애플리케이션입니다.

## 주요 기능

| 탭 | 기능 | 설명 |
|---|---|---|
| Tab 1 | [격자 생성기](docs/tab1_grating_generator.md) | 이진 격자 마스크 생성 (톱니파 기반) |
| Tab 2 | [현미경 시뮬레이터](docs/tab2_microscope_simulator.md) | OTF 기반 현미경 이미징 시뮬레이션 |
| Tab 3 | [Scheimpflug 시뮬레이터](docs/tab3_scheimpflug_simulator.md) | Homography + 밝기 감쇠 보정 |
| Tab 4 | [프로젝션 시뮬레이터](docs/tab4_projection_simulator.md) | 프로젝션 OTF + defocus 시뮬레이션 |
| Tab 5 | [FFT 이미지 분석](docs/tab5_fft_analyzer.md) | 사인파 방향 검출 + 주기 측정 |

## 설치

### 요구사항

- Python 3.9 이상
- Windows 10/11

### 자동 설치

```bash
install.bat
```

가상환경 생성, 의존성 설치, PyTorch 설치 옵션(CUDA/CPU/건너뛰기)을 안내합니다.

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
- PySide6 — GUI 프레임워크
- numpy — 수치 계산
- opencv-python — 이미지 처리
- matplotlib — 시각화
- tqdm — 진행률 표시

### 선택
- torch — GPU 가속 (Scheimpflug 거리/감쇠 맵 계산). 미설치 시 numpy로 자동 fallback

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
│   └── simulators/           # 시뮬레이션 엔진
│       ├── grating.py        # 격자 패턴 생성
│       ├── microscope.py     # 현미경 OTF 시뮬레이션
│       ├── projection.py     # 프로젝션 OTF 시뮬레이션
│       ├── scheimpflug.py    # Scheimpflug 보정
│       └── fft_analyzer.py   # FFT 이미지 분석
│
├── docs/                     # 문서
│   ├── architecture.md       # 아키텍처 개요
│   ├── tab1~tab5_*.md        # 탭별 상세 문서
│
├── bin/                      # 레거시 스크립트 (참고용)
└── output/                   # 세션별 결과 출력
```

자세한 아키텍처 설명은 [docs/architecture.md](docs/architecture.md)를 참조하세요.

## 데이터 흐름

```
[Tab 1] 격자 생성 → BMP
            ↓
[Tab 2] 현미경 시뮬레이션     [Tab 4] 프로젝션 시뮬레이션
                                      ↓
                              [Tab 3] Scheimpflug 보정

[Tab 5] FFT 분석 ← 임의 이미지 (독립)
```

## 출력

모든 결과는 `output/YYYYMMDD_HHMMSS/` 형식의 세션 폴더에 저장됩니다.
