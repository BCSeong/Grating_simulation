# Tab 4: Projection Simulator (프로젝션 시뮬레이터)

## 개요

프로젝션 광학계의 이미징을 시뮬레이션합니다. 초점 상태(focused)와 탈초점(defocused) OTF를 각각 계산하여, 격자 이미지가 프로젝터를 통해 투영되었을 때의 결과를 생성합니다. PSF through-focus 전파도 지원합니다.

## 시뮬레이터 클래스

**파일**: `grating_simulator/simulators/projection.py`
**클래스**: `Projection_image_simulator`

### 주요 파라미터

| 파라미터 | 설명 |
|---|---|
| `z0_WD_lens_to_plane_mm` | 작업 거리 (렌즈 → 물체, mm) |
| `z1_WD_defocus_lens_to_plane_mm` | 탈초점 거리 (렌즈 → 물체, mm) |
| `pupil_diameter_mm` | 동공 직경 (mm) |
| `wavelength` | 파장 목록 (μm) |
| `spectrum_step` | 파장 스텝 (nm) |
| `edge_remover_factor` | 가장자리 제거 비율 |
| `resize` | 결과 이미지 리사이즈 비율 |

### 메서드

| 메서드 | 설명 |
|---|---|
| `load_image(bmp_path)` | 격자 BMP 로드 |
| `load_grating_parameters(json_path)` | 격자 파라미터 (주기, 샘플링) 로드 |
| `initialize_optics()` | 배율, NA, DOF, 주파수 격자 계산 |
| `check_simulation_condition()` | 컷오프/Nyquist/리사이즈 검증 |
| `calculate_OTF(user_z1_defo_mm)` | 초점 + 탈초점 OTF 계산 |
| `perform_OTF()` | 이미지에 OTF 적용 + 가장자리 크롭 |
| `resize_result()` | 결과 이미지 다운샘플링 |
| `plot_matplotlib_image_crs()` | 2×2 cross-section + FFT figure |
| `psf_prop()` | DOF 범위 through-focus PSF 전파 |
| `plot_matplotlib_psf_crs()` | 축방향 PSF 강도 프로파일 |
| `save_image(output_dir)` | 결과 BMP 저장 |
| `save_parameters_json_dict(json_path)` | 파라미터 JSON 저장 |
| `run(bmp_path, json_path)` | 전체 파이프라인 |

### 핵심 수학

1. **배율**: `M = z1 / z0` (박렌즈 공식)
2. **NA**: `NA = pupil_diameter / (2 × z0)`
3. **OTF 계산**: 동공 자기상관, 다색 파장 가중 평균
4. **Defocus**: `W_defocus = (Δz × NA²) / (2λ)` — 근축 탈초점 위상
5. **이미징**: `결과 = iFFT(FFT(입력) × OTF)`
6. **PSF 전파**: DOF 범위 내 defocus 스윕, 축방향 PSF 강도 계산

## GUI 조작 순서

1. **Load Image** → 격자 BMP 로드
2. **Load Parameters** → 격자 파라미터 JSON 로드
3. 광학 파라미터 설정 (z0, z1, pupil, wavelength 등)
4. **Initialize** → 광학 초기화
5. **Calculate OTF** → focused + defocused OTF 계산
6. **Generate Image** → 프로젝션 이미지 생성
7. **Plot Cross Section** → 교차 단면 분석 팝업
8. **PSF Propagation** → through-focus PSF 계산
9. **Plot PSF Cross Section** → PSF 프로파일 표시

## 모듈 레벨 함수

| 함수 | 설명 |
|---|---|
| `myFFT(ndarray)` | 중심이동 FFT |
| `myiFFT(ndarray)` | 중심이동 역FFT |
| `affine_scale_image_with_warp(img, scale)` | 중심 기준 어파인 스케일링 |

## 관련 파일

- 입력: Tab 1에서 생성된 `grating_*.bmp` + `grating_parameters.json`
- 출력: `output/YYYYMMDD_HHMMSS/projected_*.bmp`, `defocused_*.bmp`, `*_parameters.json`
