# Tab 3: Scheimpflug Simulator (Scheimpflug 보정 시뮬레이터)

## 개요

Scheimpflug 조건 하에서 투영 이미지의 기하학적 왜곡(homography)과 밝기 감쇠(brightness attenuation)를 시뮬레이션합니다. 카메라가 기울어진 평면을 촬영할 때 발생하는 사다리꼴 왜곡과 거리에 따른 밝기 변화를 보정합니다.

## 시뮬레이터 클래스

**파일**: `grating_simulator/simulators/scheimpflug.py`
**클래스**: `Scheimpflug_simulator`

### 주요 파라미터

| 파라미터 | 설명 |
|---|---|
| `x_rot_deg`, `y_rot_deg` | 기울기 각도 (X축, Y축, 도) |
| `d0` | 물체 거리 (mm) |
| `di` | 이미지 거리 (mm) — 박렌즈 공식에서 계산 |
| `K` | 카메라 내부 행렬 (3×3) |
| `homographyMTX` | Homography 행렬: `H = K · K_h · R_tilt · K^{-1}` |
| `pad` | 이미지 패딩 (정수) |
| `pupil_diameter_mm` | 동공 직경 (mm) |

### 메서드

| 메서드 | 설명 |
|---|---|
| `load_image(bmp_path)` | 프로젝션 결과 이미지 로드 |
| `load_proj_image_parameters(json_path)` | z0, z1, defocus, pixel_size 파라미터 로드 |
| `initialize_optics()` | 카메라 행렬, homography 계산 |
| `check_simulation_condition()` | 각도 범위, 배율, 거리 검증 |
| `apply_homography()` | 이미지에 homography 변환 적용 (cv2.warpPerspective) |
| `compute_pixel_to_camera_distance_and_scale()` | 거리/감쇠 맵 계산 (GPU/CPU 자동 선택) |
| `imshow_result()` | 결과 figure 생성 (warped + cross-section) |
| `run(bmp_path, json_path)` | 전체 파이프라인 실행 |

### GPU/CPU 백엔드

거리 맵과 밝기 감쇠 계산은 두 가지 백엔드를 지원합니다:

| 메서드 | 백엔드 | 조건 |
|---|---|---|
| `_compute_distance_and_scale_gpu(torch)` | torch (CUDA/CPU) | torch 설치됨 |
| `_compute_distance_and_scale_cpu()` | numpy | torch 미설치 (fallback) |

`compute_pixel_to_camera_distance_and_scale()` 래퍼가 자동으로 적절한 백엔드를 선택합니다.

### 핵심 수학

1. **Homography**: `H = K · K_h · R_tilt · K^{-1}`
   - `K`: 카메라 내부 행렬 (focal length, principal point)
   - `R_tilt`: 3D 회전 행렬 (x, y 기울기)
   - `K_h`: 평면 매핑 행렬

2. **역제곱 감쇠**: `inv_sqr = 1 / (d_image / d_object)²`
   - 기울어진 평면의 각 픽셀별 물체/이미지 거리 비율

3. **cos⁴ 감쇠**: 입사각에 따른 자연 비네팅(natural vignetting)

### 출력

- `self.warped_image`: homography 적용된 이미지
- `self.inv_sqr_raw`: 역제곱 밝기 감쇠 맵 (정규화)
- `self.attenuation_map`: cos⁴ 감쇠 맵

## GUI 조작 순서

1. **1. Load Image** → 프로젝션 BMP 로드
2. **2. Load Params** → 프로젝션 파라미터 JSON 로드
3. 기울기 각도 설정 (X, Y Projection Angle)
4. **3. Initialize** → 광학 초기화 + 조건 검증
5. **4. Apply Homography** → 이미지 왜곡 적용
6. **5. Compute Brightness** → 밝기 감쇠 계산 + 최종 결과 생성
7. **6. Plot CrossSection** → 교차 단면 figure 표시

## 모듈 레벨 유틸리티 함수

| 함수 | 설명 |
|---|---|
| `convert_angles(angle, magnification, mode)` | 물체/투영 공간 간 각도 변환 |
| `add_poisson_noise(image)` | 포아송 노이즈 추가 |
| `add_gaussian_noise(image, mean, std)` | 가우시안 노이즈 추가 |
| `add_speckle_noise(image, std_factor)` | 스페클 노이즈 추가 |
| `estimate_sine_wave_params(image)` | 히스토그램 CDF 기반 min/max 추정 |
| `normalize_sim_image(sim_img, min_val, max_val)` | 시뮬레이션 이미지 강도 범위 정규화 |
| `find_crop_region(sim_img, exp_img)` | 템플릿 매칭 기반 최적 크롭 위치 탐색 |

## 관련 파일

- 입력: Tab 4에서 생성된 프로젝션 BMP + 파라미터 JSON
- 출력: `output/YYYYMMDD_HHMMSS/scheimpflug_*.bmp`, `*_parameters.json`
