# Tab 4: Projection Simulator (프로젝션 시뮬레이터)

**소스 파일**: `grating_simulator/simulators/projection.py`

## 개요

프로젝션 광학계의 이미징을 시뮬레이션합니다. 초점(focused)과 탈초점(defocused) 상태의 OTF를 각각 계산하여, 격자 이미지가 프로젝터를 통해 투영되었을 때의 결과를 생성합니다. 근축(paraxial) 탈초점 위상 모델을 사용하며, through-focus PSF 전파도 지원합니다.

---

## 모듈 레벨 상수

| 이름 | 값 | 설명 |
|---|---|---|
| `m` | `1/1000` | 미터 → 밀리미터 변환 |
| `mm` | `1` | 밀리미터 기본 단위 |
| `um` | `1000` | 마이크로미터 → 밀리미터 변환 계수 |

---

## 모듈 레벨 함수

### `myFFT(ndarray)`

중심이동 순방향 FFT. Tab 2의 `myFFT`와 동일한 구현입니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `ndarray` | `numpy.ndarray` | 입력 배열 |

**반환값:** `numpy.ndarray` (complex) — 중심이동된 FFT 결과

**연산:** `fftshift(fftn(ifftshift(input)))`

---

### `myiFFT(ndarray)`

중심이동 역방향 FFT.

**파라미터/반환값:** `myFFT`와 대칭. `fftshift(ifftn(ifftshift(input)))`

---

### `affine_scale_image_with_warp(img, scale, maintain_size=True)`

이미지 중심 기준으로 어파인 스케일링을 수행합니다.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `img` | `ndarray` | — | 입력 이미지 (그레이스케일 또는 컬러) |
| `scale` | `float` | — | 스케일 팩터. >1이면 확대, <1이면 축소 |
| `maintain_size` | `bool` | `True` | `True`: 출력 크기 = 입력 크기 (패딩/크롭). `False`: 출력 크기 = 입력 × scale |

**반환값:**

| 타입 | 설명 |
|---|---|
| `ndarray` | 스케일링된 이미지. border는 0으로 채움 |

**내부 구현:** `cv2.getRotationMatrix2D(center, angle=0, scale=scale)` + `cv2.warpAffine`

**용도:** PSF 전파 시 탈초점 PSF를 초점 격자에서 탈초점 격자로 리스케일

---

## 클래스: `Projection_image_simulator`

### 생성자

```python
Projection_image_simulator()
```

기본 프로젝션 파라미터(z0=31.5mm, z1=630mm, pupil=2mm)로 초기화됩니다.

---

## 속성

### 사용자 입력 파라미터 — 프로젝션 광학

| 속성 | 타입 | 기본값 | GUI 위젯 | 설명 |
|---|---|---|---|---|
| `z0_mm` | `float` | `31.5` | — | 렌즈에서 마스크(물체)까지 거리 (mm) |
| `z1_mm` | `float` | `630.0` | — | 렌즈에서 투영면(이미지)까지 거리 (mm) |
| `pupil_diameter_mm` | `float` | `2.0` | — | 프로젝터 렌즈 동공 직경 (mm) |
| `defocus_z1_mm` | `float` | `1.0` | — | 초점면에서의 탈초점 거리 (mm). 투영면 이동량 |
| `resize_factor` | `float` | `1.0` | — | 결과 이미지 높이 다운샘플 비율 |
| `resize_factor_along_width` | `float` | `1.0` | — | 결과 이미지 너비 다운샘플 비율 |

### 사용자 입력 파라미터 — 가장자리 제거

| 속성 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `clear_board_toggle` | `bool` | `True` | 가장자리 크롭 사용 여부 |
| `clear_board_factor` | `float` | `1.0` | 크롭 폭 = `period_of_saw / mask_sampling_width_in_um × factor` (px) |

### 사용자 입력 파라미터 — 스펙트럼

| 속성 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `custom_spectrum_toggle` | `bool` | `False` | 커스텀 스펙트럼 사용 여부 |
| `spectrum_min` | `float` | `0.5876` | 최소 파장 (μm) |
| `spectrum_max` | `float` | `0.5876` | 최대 파장 (μm) |
| `spectrum_step` | `float` | `0.0` | 파장 스텝 (nm). 0이면 단색 |
| `wvls_um` | `list[float]` | `[0.5876]` | 파장 목록 (μm) |

### 사용자 입력 파라미터 — 기타

| 속성 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `header_prefix` | `str` | `''` | 파일 저장 prefix |
| `save_result_toggle` | `bool` | `True` | 자동 저장 여부 |
| `mask_path` | `str` | `''` | 마스크 이미지 경로 |
| `debug_mode` | `bool` | `False` | 디버그 모드 |

### 로드/계산된 속성

| 속성 | 타입 | 설명 |
|---|---|---|
| `H`, `W` | `int` | 로드된 이미지 크기 |
| `H_mm`, `W_mm` | `float` | 이미지 물리적 크기 (mm) |
| `mask_float` | `ndarray` (float32) | 로드된 마스크 이미지 |
| `mask_sampling_width_in_um` | `float` | 마스크 픽셀 크기 (μm/px) |
| `period_of_saw` | `float` | 톱니파 주기 (μm) |

### 계산된 광학 파라미터 (`initialize_optics()` 이후)

| 속성 | 타입 | 설명 |
|---|---|---|
| `magnification_defo` | `float` | 탈초점 배율 = `(z1 + defocus_z1) / z0` |
| `obj_space_f_number` | `float` | 물체측 F수 = `0.5 / ((pupil_diameter/2) / z0)` |
| `img_space_na` | `float` | 이미지측 NA = `(pupil_diameter/2) / z1` |
| `DOF_bidirec_mm` | `float` | 양방향 초점심도 = `λ / NA²` (mm) |
| `projection_sampling_width_in_um` | `float` | 투영면 픽셀 크기 = `mask_sampling × magnification` (μm/px) |
| `projection_H_mm`, `projection_W_mm` | `float` | 투영면 이미지 크기 (mm) |
| `resized_H`, `resized_W` | `int` | 리사이즈 후 이미지 크기 (px) |
| `resized_sampling_width_in_um` | `float` | 리사이즈 후 픽셀 크기 (μm/px) |
| `resized_H_mm`, `resized_W_mm` | `float` | 리사이즈 후 이미지 크기 (mm) |
| `dkx`, `dky` | `float` | 주파수 샘플링 간격 (cycles/μm) |
| `RHO` | `ndarray` | 방사형 공간주파수 격자 (cycles/μm) |
| `W_crop` | `int` | 가장자리 제거 후 너비 (px) |

### 결과 속성

| 속성 | 타입 | shape | 설명 |
|---|---|---|---|
| `eff_OTF` | `ndarray` (complex) | `(H, W)` | 초점 OTF (정규화) |
| `eff_OTF_uint` | `ndarray` (uint8) | `(H, W)` | 초점 OTF 시각화 |
| `eff_defocus_OTF` | `ndarray` (complex) | `(H, W)` | 탈초점 OTF |
| `eff_defocus_OTF_uint` | `ndarray` (uint8) | `(H, W)` | 탈초점 OTF 시각화 |
| `projected_mask_uint` | `ndarray` (uint8) | `(H, W_crop)` | 초점 투영 이미지 |
| `defocused_projected_mask_uint` | `ndarray` (uint8) | `(H, W_crop)` | 탈초점 투영 이미지 |
| `resized_result_uint` | `ndarray` (uint8) | `(resized_H, resized_W)` | 리사이즈된 초점 결과 |
| `resized_defocused_result_uint` | `ndarray` (uint8) | `(resized_H, resized_W)` | 리사이즈된 탈초점 결과 |
| `psf_crs_uint` | `ndarray` (uint8) | `(z_step, slice_width)` | Through-focus PSF 단면 |
| `z_list` | `ndarray` | `(z_step,)` | PSF 전파 z 위치 목록 (mm) |

---

## 메서드

### `load_image(bmp_path)`

격자 BMP 이미지를 로드합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `bmp_path` | `str` | 그레이스케일 BMP 파일 경로 |

**설정되는 속성:** `mask_bmp`, `mask_float` (float32), `H`, `W`

---

### `load_grating_parameters(json_path)`

격자 파라미터 JSON에서 주기와 샘플링 정보를 읽습니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `json_path` | `str` | Tab 1의 `grating_parameters.json` 경로 |

**읽어오는 키:** `mask_sampling_width_in_um`, `period_of_saw`

---

### `save_parameters_json_dict(json_path=None)`

현재 파라미터를 JSON 파일로 저장합니다.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `json_path` | `str` or `None` | `None` | 저장 경로. `None`이면 `{header_prefix}Projection_params.json` |

**저장되는 키:** `header_prefix`, `z0_mm`, `z1_mm`, `pupil_diameter_mm`, `defocus_z1_mm`, `resize_factor`, `resize_factor_along_width`, `clear_board_toggle`, `clear_board_factor`, 스펙트럼 파라미터, 계산된 리뷰 파라미터 등 (총 22개 키)

---

### `update_parameters_json_dict(file_path)`

JSON 파일의 모든 키-값 쌍을 인스턴스 속성으로 설정합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `file_path` | `str` | JSON 파일 경로 |

---

### `initialize_optics()`

광학 파라미터를 계산하고 주파수 도메인 격자를 구축합니다.

**파라미터:** 없음

**사전 조건:**
- `load_image()` 호출 완료 (`H`, `W`, `mask_float` 필요)
- `mask_sampling_width_in_um ≠ 0` (직접 설정 또는 `load_grating_parameters()`)

**수식:**

```
magnification = (z1 + defocus_z1) / z0
obj_space_f_number = 0.5 / ((pupil_diameter / 2) / z0)
img_space_na = (pupil_diameter / 2) / z1
DOF = λ_center / NA²    (양방향, mm)

projection_pixel = mask_pixel × magnification
dkx = 1 / (W × projection_pixel)    [cycles/μm]
dky = 1 / (H × projection_pixel)    [cycles/μm]
```

---

### `check_simulation_condition()`

시뮬레이션 유효성을 검증합니다.

**검증 항목:**

1. **컷오프 vs. Nyquist**: `NA/λ_min < max(RHO)/5` — OTF가 주파수 격자 내에 충분한 여유로 존재
2. **해상도**: `NA/λ_max > min(dkx, dky)×4` — OTF 형태를 해상할 충분한 샘플
3. **리사이즈 팩터**: 양수 확인

---

### `calculate_OTF(user_z1_defo_mm=None, disable_tqdm=False, progress_callback=None)`

초점 + 탈초점 OTF를 계산합니다. 다색(polychromatic) 지원.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `user_z1_defo_mm` | `float` or `None` | `None` | 사용자 지정 탈초점 거리 (mm). `None`이면 `self.defocus_z1_mm` 사용. PSF 전파에서 스윕할 때 사용 |
| `disable_tqdm` | `bool` | `False` | 진행률 표시 비활성화 (PSF 전파 내부 루프에서 사용) |
| `progress_callback` | `callable` or `None` | `None` | 진행률 콜백. 시그니처: `callback(current: int, total: int, message: str)`. 각 파장 반복마다 호출됨. 취소 시 `CancellationError` 발생 |

**반환값:** 없음

**알고리즘:**

각 파장 `λ`에 대해:

1. **컷오프 주파수**: `cf = img_space_na / λ`

2. **동공 함수**: `P(ρ) = 1 if ρ ≤ cf, else 0`

3. **탈초점 위상 (근축 모델)**:
   ```
   Φ(ρ) = exp(-iπ × λ × Δz × ρ²)
   ```
   여기서 `Δz = defocus_z1_mm × 1000` (μm 변환), `ρ` = 공간주파수 (cycles/μm)

   > **중요**: numpy FFT는 `ν` (cycles/length) 기반이므로 위상에 `π`가 사용됩니다 (`2π`가 아님).
   > 각주파수 `ω = 2πν`를 사용하면 `exp(-i2πλzρ²)`가 되어 위상 곡률이 2배가 됩니다.

4. **PSF 계산**:
   - 초점: `PSF_focus = |iFFT(P)|²`
   - 탈초점: `PSF_defocus = |iFFT(P × Φ)|²`

5. **OTF**: `OTF = FFT(PSF)`

6. **다색 합성**:
   ```
   eff_OTF = Σ OTF_focus(λ_i)              [정규화: max(|eff_OTF|)]
   eff_defocus_OTF = Σ OTF_defocus(λ_i)    [eff_OTF의 에너지로 정규화]
   ```

**설정되는 속성:** `eff_OTF`, `eff_OTF_uint`, `eff_defocus_OTF`, `eff_defocus_OTF_uint`, `eff_Phi_angle_uint`, `eff_defo_psf`

---

### `perform_OTF()`

마스크 이미지에 초점/탈초점 OTF를 적용합니다.

**파라미터:** 없음

**수식:**
```
projected = |FFT(iFFT(mask) × eff_OTF)|
defocused = |FFT(iFFT(mask) × eff_defocus_OTF)|
```

**가장자리 크롭** (`clear_board_toggle=True`):
양쪽에서 `board_crop_px` 픽셀을 제거합니다.
```
board_crop_px = int(period_of_saw / mask_sampling_width_in_um × clear_board_factor)
```

**설정되는 속성:** `projected_mask_uint`, `defocused_projected_mask_uint` (uint8, 0-255 clip)

---

### `resize_result()`

투영 결과를 다운샘플링합니다.

**파라미터:** 없음

**내부 구현:** `cv2.resize(..., interpolation=cv2.INTER_AREA)` — 축소 시 안티앨리어싱 효과

**설정되는 속성:** `resized_result_uint`, `resized_defocused_result_uint`

---

### `save_image(path=None, output_dir=None)`

리사이즈된 결과 이미지를 BMP로 저장합니다.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `path` | `str` or `None` | `None` | 저장 경로. `None`이면 `{header_prefix}projected_image.bmp` |
| `output_dir` | `str` or `None` | `None` | 저장 디렉토리 |

**저장 파일:**
- `{prefix}projected_image.bmp` — 초점 결과
- `{prefix}defocused_projected_image.bmp` — 탈초점 결과

---

### `plot_matplotlib_image_crs()`

탈초점 결과의 수직/수평 교차 단면과 FFT 스펙트럼을 2×2 figure로 생성합니다.

**파라미터:** 없음

**반환값:**

| 타입 | 설명 |
|---|---|
| `matplotlib.Figure` | 2×2 figure |

**Figure 구성:**

| 위치 | 내용 | 축 |
|---|---|---|
| `[0,0]` | 수직 교차 단면 (중앙 열) | px (하단), mm (상단) |
| `[0,1]` | 수평 교차 단면 (중앙 행) | px (하단), mm (상단) |
| `[1,0]` | 수직 FFT 스펙트럼 | 공간주파수 (cycles/px), 피크 주기 주석 |
| `[1,1]` | 수평 FFT 스펙트럼 | 공간주파수 (cycles/px), 피크 주기 주석 |

**피크 주석 형식:** `Period = {period_px:.1f} px ({period_mm:.4f} mm)`

---

### `psf_prop(progress_callback=None)`

Through-focus PSF 전파를 계산합니다. DOF 범위를 64 스텝으로 스윕하면서 각 z 위치에서의 PSF를 계산합니다.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `progress_callback` | `callable` or `None` | `None` | 진행률 콜백. 시그니처: `callback(current: int, total: int, message: str)`. z_list의 각 z 위치마다 호출됨 (64 스텝). 취소 시 `CancellationError` 발생 |

**알고리즘:**

1. z 범위 설정: `z ∈ [-DOF, +DOF]`, 64 스텝
2. `defocus_z1_mm = 0`으로 설정, `initialize_optics()` 재호출 (초점 격자 기준)
3. 각 z에 대해:
   - `calculate_OTF(user_z1_defo_mm=z)` — 해당 z에서의 탈초점 OTF 계산
   - `scale = (z1 + z) / z1` — 초점→탈초점 격자 스케일 팩터
   - `affine_scale_image_with_warp(psf, scale)` — PSF 리스케일
4. 축방향 PSF 단면 추출: 이미지 중심에서 수직 또는 수평 슬라이스

**설정되는 속성:**

| 속성 | 타입 | shape | 설명 |
|---|---|---|---|
| `z_list` | `ndarray` | `(64,)` | z 위치 (mm, DOF 기준) |
| `psf_crs_uint` | `ndarray` (uint8) | `(64, slice_width)` | 축방향 PSF 단면 |

---

### `plot_matplotlib_psf_crs()`

축방향 PSF 강도 프로파일을 생성합니다.

**파라미터:** 없음

**반환값:**

| 타입 | 설명 |
|---|---|
| `matplotlib.Figure` | 축방향 PSF 프로파일 (x: z1+z [mm], y: intensity [0-255]) |

---

### `run(bmp_path, json_path, parameters=None)`

전체 프로젝션 시뮬레이션 파이프라인을 실행합니다.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `bmp_path` | `str` | — | 격자 BMP 경로 |
| `json_path` | `str` | — | 격자 파라미터 JSON 경로 |
| `parameters` | `dict` or `None` | `None` | 추가 파라미터 |

**실행 순서:**
1. `load_image(bmp_path)`
2. `load_grating_parameters(json_path)`
3. (조건) `update_parameters()`
4. `initialize_optics()`
5. `check_simulation_condition()`
6. `calculate_OTF()`
7. `perform_OTF()`
8. `resize_result()`
9. `save_image()`
10. `plot_matplotlib_image_crs()`
11. `psf_prop()`
12. `plot_matplotlib_psf_crs()`

---

### `check_psf_prop(progress_callback=None)`

이미지 로드 없이 광학 초기화와 PSF 전파만 실행합니다. 광학 파라미터 변경 후 빠른 PSF 확인용.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `progress_callback` | `callable` or `None` | `None` | 진행률 콜백. `psf_prop()`에 그대로 전달됨. 시그니처: `callback(current: int, total: int, message: str)`. 취소 시 `CancellationError` 발생 |

**실행 순서:** `initialize_optics()` → `check_simulation_condition()` → `psf_prop(progress_callback)`

---

## GUI 조작 순서

1. **Load Image** → 격자 BMP 로드
2. **Load Parameters** → 격자 파라미터 JSON 로드
3. 광학 파라미터 설정 (z0, z1, pupil, defocus, spectrum, resize 등)
4. **Initialize** → 광학 초기화 + 조건 검증
5. **Calculate OTF** → 초점/탈초점 OTF 계산, OTF 이미지 표시
6. **Generate Image** → 투영 이미지 생성 + 리사이즈 + 자동 저장
7. **Plot Cross Section** → 교차 단면 + FFT 분석 팝업
8. **PSF Propagation** → Through-focus PSF 계산
9. **Plot PSF Cross Section** → 축방향 PSF 프로파일 팝업

## 출력 파일

| 파일 | 설명 |
|---|---|
| `{prefix}projected_image.bmp` | 초점 투영 결과 (리사이즈 후, uint8) |
| `{prefix}defocused_projected_image.bmp` | 탈초점 투영 결과 (리사이즈 후, uint8) |
| `{prefix}Projection_params.json` | 프로젝션 파라미터 전체 (Tab 3에서 로드) |

---

## 이론적 배경

### 근축 탈초점 위상 모델

numpy FFT의 주파수 변수 `ν` (cycles/μm)를 사용할 때, 탈초점 전달 함수:

```
H(ν) = exp(-iπ × λ × Δz × ν²)
```

- `λ`: 파장 (μm)
- `Δz`: 탈초점 거리 (μm)
- `ν²`: `KX² + KY²` (cycles/μm)²

지수에 `π`가 한 개만 있음에 주의. `2π`를 사용하면 위상 곡률이 2배가 되어 부정확합니다.

### OTF 정규화

초점 OTF와 탈초점 OTF는 동일한 에너지 기준으로 정규화됩니다:

```
norm_factor = max(|Σ OTF_focus(λ_i)|)
eff_OTF = Σ OTF_focus / norm_factor
eff_defocus_OTF = Σ OTF_defocus / norm_factor   ← 같은 norm_factor 사용
```

이렇게 하면 탈초점 OTF의 에너지 감소가 초점 OTF 대비 정확하게 반영됩니다.

### PSF 리스케일링

탈초점 시 배율이 변하므로 (`scale = (z1+Δz)/z1`), 초점 격자에서 계산된 PSF를 탈초점 격자로 변환해야 합니다. `affine_scale_image_with_warp`로 중심 기준 리스케일을 수행합니다.
