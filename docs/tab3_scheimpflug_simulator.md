# Tab 3: Scheimpflug Simulator (Scheimpflug 보정 시뮬레이터)

**소스 파일**: `grating_simulator/simulators/scheimpflug.py`

## 개요

Scheimpflug 조건 하에서 투영 이미지의 기하학적 왜곡(homography)과 밝기 감쇠(brightness attenuation)를 시뮬레이션합니다. 카메라 축에 대해 기울어진 평면에 투영된 패턴이 어떻게 왜곡되고, 거리 차이에 의해 밝기가 어떻게 변하는지를 모델링합니다.

---

## 모듈 레벨 함수

### `evaluate_reprojection_error(K, Kh, R_tilt, H, d0, image_size, num_samples=5)`

물리적 투영과 homography 투영 간의 재투영 오차를 계산합니다.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `K` | `ndarray` (3×3) | — | 카메라 내부(intrinsic) 행렬 |
| `Kh` | `ndarray` (3×3) | — | 평면 매핑 행렬 |
| `R_tilt` | `ndarray` (3×3) | — | 3D 회전 행렬 |
| `H` | `ndarray` (3×3) | — | Homography 행렬 `K @ Kh @ R_tilt @ K⁻¹` |
| `d0` | `float` | — | 카메라 중심에서 원래 평면까지 거리 (mm) |
| `image_size` | `tuple` (int, int) | — | `(width, height)` 픽셀 |
| `num_samples` | `int` | `5` | 축당 샘플 수. 총 `num_samples²` 개 점 평가 |

**반환값:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `rmse` | `float` | RMS 재투영 오차 (px) |
| `max_err` | `float` | 최대 재투영 오차 (px) |

**알고리즘:**
각 샘플 픽셀 (u, v)에 대해:
1. K⁻¹로 방향 벡터 d 계산 → 물체 거리 d0에서 3D 점 X₁ 구함
2. **물리적 투영**: `p_true = (K @ Kh @ R_tilt @ X₁) / z`
3. **Homography 투영**: `p_est = (H @ [u, v, 1]ᵀ) / z`
4. 두 결과의 유클리드 거리를 오차로 측정

---

### `is_rotation_matrix(R, tol=1e-6)`

행렬이 진정한 회전 행렬(proper rotation matrix)인지 검증합니다.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `R` | `ndarray` (3×3) | — | 검증할 행렬 |
| `tol` | `float` | `1e-6` | 오차 허용치 (Frobenius 노름 기준) |

**반환값:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `is_rot` | `bool` | 회전 행렬이면 `True` |
| `orth_error` | `float` | 직교성 오차: `‖RᵀR − I‖_F` |
| `det_error` | `float` | 행렬식 오차: `|det(R) − 1|` |

**검증 조건:**
- `RᵀR ≈ I` (직교 행렬)
- `det(R) ≈ +1` (proper rotation, 반사 아님)

---

### `stretch_image_to_square(img)`

이미지를 정사각형으로 리사이즈합니다. 큰 쪽의 치수에 맞춰 작은 쪽을 확장합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `img` | `ndarray` | 입력 이미지 (그레이스케일 또는 컬러) |

**반환값:**

| 타입 | 설명 |
|---|---|
| `ndarray` | 정사각형으로 리사이즈된 이미지 |

**주의:** 비율이 유지되지 않습니다. `max(H, W) × max(H, W)` 크기로 변환됩니다.

---

### `rotate_image(img, N_deg)`

이미지를 중심 기준으로 회전합니다. 출력 크기는 입력과 동일합니다 (잘리는 영역 발생 가능).

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `img` | `ndarray` | 입력 이미지 |
| `N_deg` | `float` | 회전 각도 (도, 반시계 방향 양수) |

**반환값:**

| 타입 | 설명 |
|---|---|
| `ndarray` | 회전된 이미지 (입력과 동일 크기) |

**내부 구현:** `cv2.getRotationMatrix2D` + `cv2.warpAffine`

---

### `sample_pixels(w, h, num_samples=5)`

이미지 영역에서 균등 간격의 픽셀 좌표를 생성하는 제너레이터입니다.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `w` | `int` | — | 이미지 너비 (px) |
| `h` | `int` | — | 이미지 높이 (px) |
| `num_samples` | `int` | `5` | 축당 샘플 수 |

**반환값 (Yields):**

| 타입 | 설명 |
|---|---|
| `tuple` (float, float) | `(u, v)` 픽셀 좌표. 총 `num_samples²` 개 |

---

### `create_mask_checkerboard(rows, cols, square_size_px)`

체크보드 패턴 이미지를 생성합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `rows` | `int` | 체크보드 행 수 |
| `cols` | `int` | 체크보드 열 수 |
| `square_size_px` | `int` | 각 정사각형의 크기 (px) |

**반환값:**

| 타입 | shape | 설명 |
|---|---|---|
| `ndarray` (uint8) | `(rows×square_size_px, cols×square_size_px)` | 체크보드 이미지. 밝은 칸=255, 어두운 칸=64 |

---

### `convert_angles(angle_value_deg, magnification, mode='to_projection')`

물체 공간과 투영(이미지) 공간 간의 각도를 변환합니다. Scheimpflug 조건에 따른 기울기 각도 관계를 적용합니다.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `angle_value_deg` | `float` | — | 변환할 각도 (도) |
| `magnification` | `float` | — | 배율 `M = di / d0` |
| `mode` | `str` | `'to_projection'` | 변환 방향. `'to_projection'` 또는 `'to_scheimpflug'` |

**반환값:**

| 타입 | 설명 |
|---|---|
| `float` | 변환된 각도 (도) |

**수식:**

- `mode='to_projection'` (물체→투영):
  ```
  θ_projection = arctan(tan(θ_object) / M)
  ```
- `mode='to_scheimpflug'` (투영→물체):
  ```
  θ_object = arctan(M × tan(θ_projection))
  ```

**예외:** `mode`가 유효하지 않으면 `ValueError`

---

### `add_poisson_noise(image)`

이미지에 포아송 노이즈를 추가합니다. 광자 수 기반의 shot noise를 모델링합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `image` | `ndarray` | 입력 이미지 (정수 값 권장) |

**반환값:**

| 타입 | 설명 |
|---|---|
| `ndarray` (uint8) | 포아송 노이즈가 적용된 이미지 |

**연산:** `output = Poisson(image)` — 각 픽셀 값을 평균으로 하는 포아송 분포에서 샘플링

---

### `add_gaussian_noise(image, mean=0, std=1)`

이미지에 가산적(additive) 가우시안 노이즈를 추가합니다.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `image` | `ndarray` | — | 입력 이미지 |
| `mean` | `float` | `0` | 가우시안 분포의 평균 |
| `std` | `float` | `1` | 가우시안 분포의 표준편차 |

**반환값:**

| 타입 | 설명 |
|---|---|
| `ndarray` (uint8) | `clip(image + N(mean, std), 0, 255)` |

---

### `add_speckle_noise(image, std_factor=0.1)`

이미지에 곱셈적(multiplicative) 스페클 노이즈를 추가합니다.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `image` | `ndarray` | — | 입력 이미지 |
| `std_factor` | `float` | `0.1` | 노이즈 강도 계수 |

**반환값:**

| 타입 | 설명 |
|---|---|
| `ndarray` (uint8) | `clip(image + image × N(0, std_factor), 0, 255)` |

---

### `estimate_sine_wave_params(image)`

히스토그램 CDF 기반으로 이미지의 유효 최소/최대 강도를 추정합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `image` | `ndarray` | 입력 이미지 (그레이스케일) |

**반환값:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `min_val` | `float` | CDF 10% 지점의 강도 값 |
| `max_val` | `float` | CDF 99.7% 지점의 강도 값 |

**용도:** 시뮬레이션 이미지를 실험 이미지의 강도 범위에 맞추기 위한 기준값 추정

---

### `normalize_sim_image(sim_img, min_val, max_val)`

시뮬레이션 이미지의 강도 범위를 지정된 범위로 정규화합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `sim_img` | `ndarray` | 시뮬레이션 이미지 |
| `min_val` | `float` | 목표 최소 강도 |
| `max_val` | `float` | 목표 최대 강도 |

**반환값:**

| 타입 | 설명 |
|---|---|
| `ndarray` | `[min_val, max_val]` 범위로 선형 정규화된 이미지 |

**수식:**
```
normalized = (img - min(img)) / (max(img) - min(img)) × (max_val - min_val) + min_val
```

---

### `find_crop_region(sim_img, exp_img)`

템플릿 매칭으로 시뮬레이션 이미지 내에서 실험 이미지와 가장 유사한 영역을 찾습니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `sim_img` | `ndarray` (uint8) | 시뮬레이션 이미지 (검색 대상) |
| `exp_img` | `ndarray` (uint8) | 실험 이미지 (템플릿) |

**반환값:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `start_x` | `int` | 매칭 영역 좌상단 x 좌표 |
| `start_y` | `int` | 매칭 영역 좌상단 y 좌표 |
| `end_x` | `int` | 매칭 영역 우하단 x 좌표 |
| `end_y` | `int` | 매칭 영역 우하단 y 좌표 |
| `max_val` | `float` | 정규화된 상관 계수 최댓값 (0~1) |

**내부 구현:** `cv2.matchTemplate(sim_img, exp_img, cv2.TM_CCOEFF_NORMED)`

---

## 클래스: `Scheimpflug_simulator`

### 생성자

```python
Scheimpflug_simulator()
```

기본 기울기 각도(x=25°, y=0°)와 패딩(100px)으로 초기화됩니다.

---

## 속성

### 사용자 입력 파라미터

| 속성 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `x_rot_deg` | `float` | `25` | X축 기울기 각도 (도). 이미지 공간(프로젝션 공간) 기준 |
| `y_rot_deg` | `float` | `0` | Y축 기울기 각도 (도) |
| `pad` | `int` | `100` | 이미지 테두리 패딩 (px). 결과 이미지에서 제거할 경계 폭 |
| `header_prefix` | `str` | `''` | 파일 저장 시 접두사 |

### 로드된 파라미터 (`load_proj_image_parameters()` 이후)

| 속성 | 타입 | 설명 |
|---|---|---|
| `z0_mm` | `float` | 렌즈에서 물체까지 거리 (mm) |
| `z1_mm` | `float` | 렌즈에서 이미지 센서까지 거리 (mm) |
| `defocus_z1_mm` | `float` | 탈초점 거리 (mm) |
| `resized_sampling_width_in_um` | `float` | 리사이즈된 픽셀 크기 (μm/px) |
| `pupil_diameter_mm` | `float` | 동공 직경 (mm) |

### 계산된 속성 (`initialize_optics()` 이후)

| 속성 | 타입 | 설명 |
|---|---|---|
| `pixel_size_mm` | `float` | 픽셀 크기 (mm/px) |
| `d0` | `float` | 물체 거리 (mm) = `z0_mm` |
| `di` | `float` | 이미지 거리 (mm) = `z1_mm + defocus_z1_mm` |
| `magnification` | `float` | 배율 = `di / d0` |
| `K` | `ndarray` (3×3) | 카메라 내부 행렬 |
| `homographyMTX` | `ndarray` (3×3) | Homography 행렬 `H = K @ K_h @ R_tilt @ K⁻¹` |
| `K_h` | `ndarray` (3×3) | 평면 매핑 행렬 |
| `R_tilt` | `ndarray` (3×3) | 3D 회전 행렬 |

### 결과 속성

| 속성 | 타입 | shape | 설명 |
|---|---|---|---|
| `proj_image_float` | `ndarray` (float32) | `(H, W)` | 로드된 이미지 |
| `warped_image` | `ndarray` (float32) | `(H, W)` | Homography 적용 후 이미지 |
| `warped_crop` | `ndarray` (float32) | `(H-2×pad, W-2×pad)` | 패딩 제거된 결과 |
| `inv_sqr_raw` | `ndarray` (float32) | `(H, W)` | 역제곱 밝기 감쇠 맵 (0~1 정규화) |
| `attenuation_map` | `ndarray` (float32) | `(H, W)` | cos⁴ 감쇠 맵 |

---

## 메서드

### `compute_camera_matrix(d0, di, pixel_size, w, h)`

박렌즈(thin lens) 모델로 카메라 내부 행렬을 계산합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `d0` | `float` | 물체 거리 (mm) |
| `di` | `float` | 이미지 거리 (mm) |
| `pixel_size` | `float` | 픽셀 크기 (mm/px) |
| `w` | `int` | 이미지 너비 (px) |
| `h` | `int` | 이미지 높이 (px) |

**반환값:**

| 타입 | 설명 |
|---|---|
| `ndarray` (3×3) | 카메라 내부 행렬 K |

**수식:**

```
f_mm = 1 / (1/d0 + 1/di)     ← 박렌즈 공식
fx = fy = f_mm / pixel_size   ← 픽셀 단위 초점거리
cx, cy = w/2, h/2             ← 주점 (이미지 중심)

K = [[fx,  0, cx],
     [ 0, fy, cy],
     [ 0,  0,  1]]
```

---

### `compute_homography_tilt_KR(rx, ry, K)`

기울기 각도에 대한 homography 행렬, 평면 매핑 행렬, 회전 행렬을 계산합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `rx` | `float` | X축 기울기 (도) |
| `ry` | `float` | Y축 기울기 (도) |
| `K` | `ndarray` (3×3) | 카메라 내부 행렬 |

**반환값:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `H` | `ndarray` (3×3) | Homography 행렬 |
| `K_h` | `ndarray` (3×3) | 평면 매핑 행렬 |
| `R_tilt` | `ndarray` (3×3) | 회전 행렬 |

**수식:**

`α = rx (rad)`, `β = ry (rad)` 로 변환 후:

```
K_h = [[cos(β)cos(α),  0,                sin(β)cos(α)],
       [0,             cos(β)cos(α),     -sin(α)      ],
       [0,             0,                 1            ]]

R_tilt = [[cos(β),   sin(α)sin(β),  -sin(β)cos(α)],
          [0,        cos(α),         sin(α)        ],
          [sin(β),  -cos(β)sin(α),   cos(β)cos(α) ]]

H = K @ K_h @ R_tilt @ K⁻¹
```

---

### `load_image(bmp_path)`

프로젝션 결과 BMP 이미지를 로드합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `bmp_path` | `str` | 그레이스케일 BMP 파일 경로 |

**설정되는 속성:** `proj_image_bmp`, `proj_image_float`, `H`, `W`

---

### `load_proj_image_parameters(json_path)`

Tab 4에서 저장된 프로젝션 파라미터 JSON을 로드합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `json_path` | `str` | 프로젝션 파라미터 JSON 파일 경로 |

**읽어오는 키:** `z0_mm`, `z1_mm`, `defocus_z1_mm`, `resized_sampling_width_in_um`, `pupil_diameter_mm`

---

### `update_parameters_json_dict(file_path)`

JSON 파일의 모든 키-값 쌍을 인스턴스 속성으로 설정합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `file_path` | `str` | JSON 파일 경로 |

---

### `initialize_optics()`

카메라 행렬과 homography를 계산합니다.

**파라미터:** 없음

**사전 조건:** `load_image()` + `load_proj_image_parameters()` 호출 완료

**설정되는 속성:** `pixel_size_mm`, `d0`, `di`, `magnification`, `K`, `homographyMTX`, `K_h`, `R_tilt`

---

### `check_simulation_condition()`

시뮬레이션 파라미터의 유효성을 검증합니다.

**검증 항목:**
- X/Y 기울기 각도: ±90° 미만
- 배율 > 0
- d0, di > 0
- pad > 0

Scheimpflug 조건에 따른 물체 공간 각도를 계산하여 출력합니다:
```
θ_object_x = -arctan(tan(θ_projection_x) / M)
θ_object_y = -arctan(tan(θ_projection_y) / M)
```

---

### `apply_homography()`

프로젝션 이미지에 homography 변환을 적용합니다.

**파라미터:** 없음

**사전 조건:** `initialize_optics()` 호출 완료

**내부 구현:** `cv2.warpPerspective(proj_image_float, homographyMTX, (W, H))`

**설정되는 속성:** `warped_image`

---

### `compute_pixel_to_camera_distance_and_scale()`

각 픽셀의 카메라까지 거리와 밝기 감쇠 맵을 계산합니다. torch(GPU)가 사용 가능하면 GPU 백엔드를, 아니면 numpy CPU 백엔드를 자동 선택합니다.

**파라미터:** 없음

**반환값:** 없음

**별칭:** `compute_pixel_to_camera_distance_and_scale_gpu` (하위 호환성)

**설정되는 속성:**

| 속성 | 타입 | shape | 범위 | 설명 |
|---|---|---|---|---|
| `inv_sqr_raw` | `ndarray` (float) | `(H, W)` | [0, 1] | 역제곱 밝기 감쇠 맵. 최댓값으로 정규화 |
| `attenuation_map` | `ndarray` (float) | `(H, W)` | [cos⁴(θ_max), 1] | cos⁴θ 자연 비네팅 맵 |

**알고리즘 (GPU/CPU 동일):**

1. **픽셀 좌표 격자 생성**: `(u, v)` for all pixels

2. **방향 벡터 계산**: `d = K⁻¹ @ [u, v, 1]ᵀ` — 각 픽셀이 가리키는 3D 방향

3. **평면(flat) 거리 맵 (d0)**:
   ```
   s = d0 / d_z               ← z=d0 평면과의 교점 스케일
   X₁ = d × s                 ← 3D 교점
   flat_distance_d0 = ‖X₁‖   ← 카메라 원점에서의 유클리드 거리
   ```

4. **평면(flat) 거리 맵 (di)**: 동일하지만 `s = di / d_z`, 수직 flip

5. **기울어진(tilted) 거리 맵**: 역 homography로 원래 좌표를 복원한 후 동일 계산
   ```
   [u', v'] = H⁻¹ @ [u, v, 1]ᵀ   ← 기울어진 평면의 원래 좌표
   d' = K⁻¹ @ [u', v', 1]ᵀ       ← 기울어진 방향 벡터
   ```

6. **역제곱 감쇠**:
   ```
   scale = tilted_d1 / tilted_d0
   inv_sqr = 1 / scale²
   inv_sqr_normalized = inv_sqr / max(inv_sqr)
   ```

7. **cos⁴ 감쇠**: 입사각에 따른 자연 비네팅
   ```
   d_normalized = d' / ‖d'‖
   cos(θ) = d_normalized_z      ← 광축과의 각도
   attenuation = cos⁴(θ)
   ```

---

### `_compute_distance_and_scale_gpu(torch)`

torch 백엔드로 거리/감쇠 맵을 계산합니다. CUDA가 사용 가능하면 GPU, 아니면 CPU에서 실행됩니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `torch` | `module` | import된 torch 모듈 (래퍼에서 전달) |

---

### `_compute_distance_and_scale_cpu()`

numpy 백엔드로 동일한 거리/감쇠 맵을 계산합니다. torch가 설치되지 않은 환경을 위한 fallback입니다.

**파라미터:** 없음

---

### `imshow_result()`

Warped 이미지와 교차 단면(cross-section)을 matplotlib figure로 생성합니다.

**파라미터:** 없음

**반환값:**

| 타입 | 설명 |
|---|---|
| `matplotlib.Figure` | 2×2 GridSpec figure: 메인 이미지 + 수평/수직 교차 단면 |

**Figure 구성:**
- `[0,0]` 메인: warped_crop 이미지 (mm 단위 축)
- `[1,0]` 하단: 수평 교차 단면 (중앙 행)
- `[0,1]` 우측: 수직 교차 단면 (중앙 열)

---

### `save_image(output_dir=None)`

워프된 이미지와 최종 결과를 BMP로 저장합니다.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `output_dir` | `str` or `None` | `None` | 저장 디렉토리 |

**저장 파일:**
- `{header_prefix}warped_image.bmp`
- `{header_prefix}scheimpflug_final_result.bmp`

---

### `save_parameters_json_dict(json_path)`

현재 Scheimpflug 파라미터를 JSON으로 저장합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `json_path` | `str` | 저장할 JSON 파일 경로 |

**저장되는 키:** `x_rot_deg`, `y_rot_deg`, `pad`, (로드된 경우) `z0_mm`, `z1_mm`, `defocus_z1_mm`, `resized_sampling_width_in_um`, `pupil_diameter_mm`

---

### `run(bmp_path, json_path, parameters=None)`

전체 Scheimpflug 시뮬레이션 파이프라인을 실행합니다.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `bmp_path` | `str` | — | 프로젝션 BMP 이미지 경로 |
| `json_path` | `str` | — | 프로젝션 파라미터 JSON 경로 |
| `parameters` | `dict` or `None` | `None` | 추가 파라미터 (사용 시 `update_parameters()` 호출) |

**실행 순서:**
1. `load_image(bmp_path)`
2. `load_proj_image_parameters(json_path)`
3. (조건) `update_parameters()`
4. `initialize_optics()`
5. `check_simulation_condition()`
6. `apply_homography()`
7. `compute_pixel_to_camera_distance_and_scale()`
8. `imshow_result()`

---

## GUI 조작 순서

1. **1. Load Image** → 프로젝션 BMP 로드
2. **2. Load Params** → 프로젝션 파라미터 JSON 로드
3. X/Y Projection Angle, Padding 등 설정
4. **3. Initialize** → 카메라 행렬 + homography 계산
5. **4. Apply Homography** → 이미지에 기하학적 왜곡 적용
6. **5. Compute Brightness** → 역제곱 + cos⁴ 밝기 감쇠 계산, 최종 결과 생성
7. **6. Plot CrossSection** → 교차 단면 팝업

## 이론적 배경

### Scheimpflug 조건

렌즈 평면, 물체 평면, 이미지 평면이 한 직선에서 만날 때 Scheimpflug 조건이 성립합니다. 이 조건에서:

- 물체 평면이 기울어져도 전체 면이 초점에 맞음
- 배율이 위치에 따라 달라짐 (사다리꼴 왜곡)
- 각도 관계: `tan(θ_object) = tan(θ_image) / M`

### Homography 모델

`H = K @ K_h @ R_tilt @ K⁻¹`

- `K`: 카메라 내부 행렬 (초점거리, 주점)
- `R_tilt`: 기울기에 의한 3D 회전
- `K_h`: 기울어진 평면의 좌표 스케일 보정
- `K⁻¹`: 픽셀 → 정규화 좌표 변환

### 밝기 감쇠

1. **역제곱 법칙**: 점광원 밝기 ∝ 1/d². 기울어진 평면의 각 점은 카메라까지 거리가 다르므로 밝기가 불균일
2. **cos⁴ 법칙**: 렌즈 중심에서 벗어난 각도 θ에서의 자연 비네팅. 조리개 투영면적(cos), 유효 입사면적(cos), 고체각(cos²)의 조합
