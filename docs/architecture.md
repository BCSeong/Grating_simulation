# 프로젝트 아키텍처

## 개요

Grating Simulator는 회절격자(grating) 패턴 생성부터 현미경/프로젝션 광학 시뮬레이션, Scheimpflug 보정, FFT 이미지 분석까지 수행하는 PySide6 기반 GUI 애플리케이션입니다. 각 기능은 독립적인 시뮬레이터 클래스로 구현되어 있으며, GUI와 분리되어 CLI에서도 사용할 수 있습니다.

---

## 디렉토리 구조

```
atp2_20250424_refactoring_GUIver/
├── run.py                          # 진입점 (Entry point)
├── run.bat                         # Windows 실행 스크립트
├── install.bat                     # 가상환경 생성 + 의존성 설치 + torch 옵션
├── requirements.txt                # Python 패키지 의존성
│
├── grating_simulator/              # 메인 패키지
│   ├── __init__.py
│   ├── app.py                      # MainWindow (전체 GUI 로직, ~1385행)
│   │
│   ├── ui/                         # UI 정의
│   │   ├── main_window.ui          # Qt Designer 원본 UI (수정 금지)
│   │   ├── main_window_ui.py       # uic 자동생성 Python 코드 (수정 금지)
│   │   └── widgets.py              # 커스텀 위젯 + 비동기 실행 인프라
│   │   #                              CancellationError, WorkerThread, ProgressDialog,
│   │   #                              PopupWindow, ZoomableGraphicsView, TextRedirector(QObject)
│   │
│   └── simulators/                 # 시뮬레이션 엔진 (GUI 독립)
│       ├── __init__.py
│       ├── grating.py              # 격자 패턴 생성기
│       ├── microscope.py           # 현미경 이미지 시뮬레이터 (OTF)
│       ├── projection.py           # 프로젝션 이미지 시뮬레이터 (OTF + defocus + PSF)
│       ├── scheimpflug.py          # Scheimpflug 보정 시뮬레이터 (homography + attenuation)
│       └── fft_analyzer.py         # FFT 이미지 분석기
│
├── bin/                            # 레거시 독립 실행 스크립트 (참고용, .gitignore 대상)
│   ├── 20M20um/                    # 실험 데이터 분석 스크립트
│   │   ├── 1_analyze_ExpData.py    # 실험 이미지 각도/주기 분석
│   │   ├── 2_calcurate_similarity_btw_sim_and_exp_imgs.py  # 시뮬레이션-실험 유사도
│   │   └── 3_figure.py             # 비교 figure 생성
│   └── *.py                        # 이전 버전 메인/시뮬레이터 스크립트
│
├── output/                         # 세션별 출력 폴더 (자동 생성, .gitignore 대상)
│   └── YYYYMMDD_HHMMSS/            # 각 실행 세션의 결과
│       ├── *.bmp                   # 이미지 결과
│       └── *.json                  # 파라미터 JSON
│
└── docs/                           # 문서
    ├── architecture.md             # 이 파일
    ├── tab1_grating_generator.md   # Tab 1 상세 문서
    ├── tab2_microscope_simulator.md # Tab 2 상세 문서
    ├── tab3_scheimpflug_simulator.md # Tab 3 상세 문서
    ├── tab4_projection_simulator.md # Tab 4 상세 문서
    ├── tab5_fft_analyzer.md        # Tab 5 상세 문서
    └── widgets.md                  # 커스텀 위젯 레퍼런스
```

---

## 탭 구성

| 탭 | 이름 | 시뮬레이터 클래스 | 소스 파일 | 입력 | 출력 |
|---|---|---|---|---|---|
| Tab 1 | Grating Generator | `Grating_generator` | `grating.py` | 파라미터 | BMP + JSON |
| Tab 2 | Microscope Simulator | `Microscope_image_simulator` | `microscope.py` | BMP + JSON (Tab 1) | BMP |
| Tab 3 | Scheimpflug Simulator | `Scheimpflug_simulator` | `scheimpflug.py` | BMP + JSON (Tab 4) | BMP + JSON |
| Tab 4 | Projection Simulator | `Projection_image_simulator` | `projection.py` | BMP + JSON (Tab 1) | BMP + JSON |
| Tab 5 | FFT Image Analysis | `FFTImageAnalyzer` | `fft_analyzer.py` | 임의 이미지 | Figure |

---

## 핵심 설계 원칙

### 1. 시뮬레이터 ↔ GUI 분리

각 시뮬레이터 클래스는 `simulators/` 디렉토리에 위치하며, GUI 코드를 참조하지 않습니다. 모든 시뮬레이터는 `run()` 메서드로 CLI에서 독립 실행 가능합니다.

```python
# CLI 사용 예시
from grating_simulator.simulators.projection import Projection_image_simulator

pis = Projection_image_simulator()
pis.pupil_diameter_mm = 3.0
pis.run('grating.bmp', 'params.json')
```

`app.py`의 `MainWindow`가 시뮬레이터를 인스턴스화하고, 버튼 클릭 → 메서드 호출 → 결과 표시를 중개합니다.

### 2. 세션 기반 출력

매 실행마다 `output/YYYYMMDD_HHMMSS/` 폴더가 생성됩니다. 모든 결과 이미지와 파라미터 JSON이 해당 세션 폴더에 저장되어, 실행 간 결과가 덮어씌워지지 않습니다.

### 3. 선택적 GPU 가속

`scheimpflug.py`의 거리/감쇠 맵 계산은 두 가지 백엔드를 지원합니다:

```python
def compute_pixel_to_camera_distance_and_scale(self):
    try:
        import torch
        self._compute_distance_and_scale_gpu(torch)  # CUDA or CPU
    except ImportError:
        self._compute_distance_and_scale_cpu()        # numpy fallback
```

torch 설치 여부에 따라 자동 선택되므로, 사용자는 신경 쓸 필요가 없습니다.

### 4. 최소 의존성

| 구분 | 패키지 | 용도 |
|---|---|---|
| 필수 | PySide6 | GUI 프레임워크 |
| 필수 | numpy | 수치 계산, FFT |
| 필수 | opencv-python | 이미지 I/O, 회전, warp |
| 필수 | matplotlib | 시각화 |
| 필수 | tqdm | 진행률 표시 |
| 선택 | torch | GPU 가속 (Scheimpflug 거리/감쇠 맵) |

scipy는 사용하지 않습니다. 이미지 회전에 `cv2.warpAffine`을 사용합니다.

### 5. auto-generated UI 보호

`main_window_ui.py`는 Qt Designer의 `.ui` 파일에서 자동 생성된 코드입니다. 이 파일은 직접 수정하지 않습니다. UI 확장이 필요한 경우 (예: Tab 5) `app.py`에서 프로그래밍 방식으로 위젯을 생성합니다.

---

## 데이터 흐름

```
[Tab 1] 격자 생성
  │  출력: grating.bmp + grating_parameters.json
  │
  ├──→ [Tab 2] 현미경 시뮬레이션
  │      입력: grating.bmp + grating_parameters.json
  │      출력: microscope_image.bmp
  │
  └──→ [Tab 4] 프로젝션 시뮬레이션
         입력: grating.bmp + grating_parameters.json
         출력: projected_image.bmp + Projection_params.json
           │
           └──→ [Tab 3] Scheimpflug 보정
                  입력: projected_image.bmp + Projection_params.json
                  출력: warped_image.bmp + scheimpflug_final_result.bmp

[Tab 5] FFT 분석 ← 임의 이미지 (독립, 파이프라인 외부)
```

### JSON 파라미터 전달

탭 간 파라미터 전달은 JSON 파일을 통해 이루어집니다:
- Tab 1 → Tab 2/4: `mask_sampling_width_in_um`, `period_of_saw`
- Tab 4 → Tab 3: `z0_mm`, `z1_mm`, `defocus_z1_mm`, `resized_sampling_width_in_um`, `pupil_diameter_mm`

---

## app.py 구조

`MainWindow.__init__`에서 5개 탭을 순서대로 초기화합니다:

```
__init__()
├── Ui_MainWindow.setupUi() — auto-generated UI 로드
├── 세션 출력 폴더 생성
│
├── Tab 1: Grating
│   ├── TextRedirector (stdout/stderr → terminal)
│   ├── ZoomableGraphicsView × 3 (ori, gen, stack)
│   ├── Grating_generator() 인스턴스
│   └── 버튼 시그널 연결
│
├── Tab 2: Microscope
│   ├── ZoomableGraphicsView × 3 (loaded, OTF, result)
│   ├── Microscope_image_simulator() 인스턴스
│   └── initialize_microscope_simulator_tab()
│
├── Tab 3: Scheimpflug
│   ├── ZoomableGraphicsView × 5 (loaded, warped, attenuation, final, cross-section)
│   ├── Scheimpflug_simulator() 인스턴스
│   └── initialize_scheimpflug_tab()
│
├── Tab 4: Projection
│   ├── ZoomableGraphicsView × 5 (loaded, OTF, projected, defocused, PSF)
│   ├── Projection_image_simulator() 인스턴스
│   └── initialize_projection_image_simulator_tab()
│
└── Tab 5: FFT Analysis
    ├── FFTImageAnalyzer() 인스턴스
    ├── _create_fft_tab_ui() — 프로그래밍 방식 UI 생성
    └── _connect_fft_signals()
```

### 비동기 실행 인프라 (Progress Bar)

무거운 시뮬레이션은 `WorkerThread`(QThread)에서 실행되어 GUI가 멈추지 않습니다.
`ProgressDialog`가 진행률을 표시하며, 사용자가 Force Stop 버튼으로 취소할 수 있습니다.

```
run_with_progress(fn, title, on_finished)
├── 모든 QPushButton 비활성화
├── ProgressDialog 생성 (모달, Force Stop 버튼)
├── WorkerThread 생성 + 시작
│   ├── fn(progress_callback=...) 실행
│   │   └── progress_callback(current, total, msg) → ProgressDialog 갱신
│   │       └── _cancelled가 True이면 CancellationError 발생
│   ├── finished → _on_task_finished(result, callback) → 정리 + callback 호출
│   ├── error → _on_task_error(error_msg) → 정리 + 에러 출력
│   └── cancelled → _on_task_cancelled() → 정리 + "Task cancelled" 출력
└── Force Stop 클릭 → _request_cancel() → worker.cancel() + 다이얼로그 UI 갱신
```

`run_with_progress`를 사용하는 핸들러 (5개):

| 탭 | 메서드 | 다이얼로그 제목 |
|---|---|---|
| Tab 2 | `calculate_OTF` | "Calculating OTF (Microscope)" |
| Tab 3 | `asw_compute_attenuation` | "Computing Brightness Attenuation" |
| Tab 4 | `prj_calculate_OTF` | "Calculating OTF (Projection)" |
| Tab 4 | `prj_generate_projected_image` | "Generating Projected Image" |
| Tab 4 | `prj_create_PSFcrs` | "PSF Propagation (64 steps)" |

### 메서드 명명 규칙

| 접두사 | 탭 | 예시 |
|---|---|---|
| (없음) | Tab 1 | `run()`, `update_parameters()`, `save_parameters()` |
| `load_microscope_*`, `calculate_OTF`, `generate_microscope_image` | Tab 2 | — |
| `asw_*` | Tab 3 | `asw_load_image()`, `asw_initialize()` |
| `prj_*` | Tab 4 | `prj_load_image()`, `prj_calculate_OTF()` |
| `fft_*` | Tab 5 | `fft_load_image()`, `fft_analyze()` |

---

## 문서 목록

| 파일 | 내용 |
|---|---|
| [architecture.md](architecture.md) | 이 파일 — 전체 아키텍처 |
| [tab1_grating_generator.md](tab1_grating_generator.md) | 격자 생성기 API |
| [tab2_microscope_simulator.md](tab2_microscope_simulator.md) | 현미경 시뮬레이터 API |
| [tab3_scheimpflug_simulator.md](tab3_scheimpflug_simulator.md) | Scheimpflug 시뮬레이터 API + 유틸리티 함수 |
| [tab4_projection_simulator.md](tab4_projection_simulator.md) | 프로젝션 시뮬레이터 API |
| [tab5_fft_analyzer.md](tab5_fft_analyzer.md) | FFT 분석기 API |
| [widgets.md](widgets.md) | 커스텀 Qt 위젯 레퍼런스 |
