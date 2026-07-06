# Tab 1: Grating Generator (격자 생성기)

## 개요

이진(binary) 격자 마스크를 생성합니다. 톱니파(sawtooth) 삼각파 기하학 기반으로 패턴을 만들고, 선택적으로 모서리를 둥글게(morphological rounding) 처리할 수 있습니다.

## 시뮬레이터 클래스

**파일**: `grating_simulator/simulators/grating.py`
**클래스**: `Grating_generator`

### 주요 파라미터

| 파라미터 | 설명 |
|---|---|
| `period_of_saw` | 톱니파 주기 (픽셀) |
| `sampling_width_in_um` | 마스크 샘플링 너비 (μm) |
| `amplitude` | 톱니파 진폭 (높이) |
| `number_of_pattern` | 수직 반복 횟수 |
| `morph_open_kernel_size` | 모서리 라운딩 커널 크기 (0이면 비활성) |
| `invert` | True면 패턴 반전 |

### 메서드

| 메서드 | 설명 |
|---|---|
| `generate_grating()` | 2D 이진 마스크 생성 |
| `image_stacker()` | 마스크를 수직으로 반복 적층 |
| `save_grating(output_dir)` | BMP 파일로 저장 (정상 + 반전) |
| `run(display, save)` | 전체 파이프라인 실행 |

### 출력

- `mask_ori`: 원본 이진 마스크 (1주기)
- `mask_gen`: 라운딩 적용된 마스크
- `buffer`: 적층된 최종 격자 이미지

## GUI 조작 순서

1. 파라미터 입력 (주기, 진폭, 반복 수 등)
2. **Initialize** → 파라미터 일관성 검증
3. **Run** → 격자 생성 + 화면 표시
4. **Save** → BMP 저장 (세션 폴더)

## 관련 파일

- 생성된 BMP: `output/YYYYMMDD_HHMMSS/grating_*.bmp`
- 파라미터 JSON: `output/YYYYMMDD_HHMMSS/grating_parameters.json`
