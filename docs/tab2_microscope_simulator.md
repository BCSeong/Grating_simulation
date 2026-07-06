# Tab 2: Microscope Simulator (현미경 시뮬레이터)

## 개요

OTF(Optical Transfer Function) 기반으로 현미경 이미징을 시뮬레이션합니다. 격자 이미지를 입력으로 받아 광학계의 주파수 응답을 적용한 결과 이미지를 생성합니다.

## 시뮬레이터 클래스

**파일**: `grating_simulator/simulators/microscope.py`
**클래스**: `Microscope_image_simulator`

### 주요 파라미터

| 파라미터 | 설명 |
|---|---|
| `NA` | 개구수 (Numerical Aperture) |
| `wavelength` | 파장 목록 (μm) |
| `mask_sampling_width_in_um` | 입력 마스크의 픽셀 크기 (μm) |

### 메서드

| 메서드 | 설명 |
|---|---|
| `load_image(path)` | 그레이스케일 BMP 이미지 로드 |
| `load_grating_parameters(path)` | 격자 파라미터 JSON에서 샘플링 정보 읽기 |
| `initialize_optics()` | 주파수 도메인 격자 (KX, KY, RHO) 구축 |
| `check_simulation_condition()` | 컷오프 주파수 vs. Nyquist 주파수 검증 |
| `calculate_OTF()` | 다색(polychromatic) OTF 계산 |
| `perform_OTF()` | 이미지에 OTF 컨볼루션 적용 |
| `run(bmp_path, json_path)` | 전체 파이프라인 실행 |

### 핵심 수학

- **주파수 격자**: `KX`, `KY` = 정규화된 공간주파수 좌표
- **동공 함수(Pupil)**: `RHO < 1` 영역 (NA로 정규화)
- **OTF**: 동공 자기상관 → 유효 전달 함수
- **이미징**: `결과 = iFFT(FFT(입력) × OTF)`

## GUI 조작 순서

1. **Load Image** → 격자 BMP 파일 선택
2. **Load Parameters** → 격자 파라미터 JSON 로드
3. **Initialize** → 광학 파라미터 설정 (NA 등)
4. **Calculate OTF** → OTF 계산 및 표시
5. **Generate Image** → 시뮬레이션 이미지 생성

## 관련 파일

- 입력: Tab 1에서 생성된 `grating_*.bmp` + `grating_parameters.json`
- 출력: `output/YYYYMMDD_HHMMSS/microscope_*.bmp`

## 모듈 레벨 함수

- `myFFT(ndarray)`: 중심이동 FFT (`fftshift → fftn → ifftshift`)
- `myiFFT(ndarray)`: 중심이동 역FFT
