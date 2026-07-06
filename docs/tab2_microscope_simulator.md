# Tab 2: Microscope Simulator (현미경 시뮬레이터)

**소스 파일**: `grating_simulator/simulators/microscope.py`

## 개요

OTF(Optical Transfer Function) 기반으로 현미경 이미징을 시뮬레이션합니다. 격자 이미지를 입력으로 받아, 지정된 NA와 파장에 대한 주파수 응답을 적용한 결과 이미지를 생성합니다. 이상적인 원형 동공(circular pupil)을 가정하며, 다색(polychromatic) 광원을 지원합니다.

---

## 모듈 레벨 함수

### `myFFT(ndarray)`

중심이동 순방향 FFT를 수행합니다. 주파수 원점이 배열 중심에 위치하도록 정렬합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `ndarray` | `numpy.ndarray` | 임의 차원의 입력 배열 |

**반환값:**

| 타입 | 설명 |
|---|---|
| `numpy.ndarray` (complex) | 중심이동된 FFT 결과. 원점이 배열 중심에 위치 |

**연산:**
```
FT = fftshift(fftn(ifftshift(input)))
```

**주의사항:**
- `ifftshift`를 먼저 적용하여 입력의 DC 성분을 인덱스 0으로 이동시킨 후 FFT 수행
- 결과에 `fftshift`를 적용하여 DC가 중심에 오도록 복원
- `np.fft.fftn` 사용: N차원 FFT (2D 이미지에 적용 시 2D FFT)

---

### `myiFFT(ndarray)`

중심이동 역방향 FFT를 수행합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `ndarray` | `numpy.ndarray` (complex) | 중심이동된 주파수 도메인 데이터 |

**반환값:**

| 타입 | 설명 |
|---|---|
| `numpy.ndarray` (complex) | 공간 도메인으로 복원된 결과 |

**연산:**
```
iFT = fftshift(ifftn(ifftshift(input)))
```

---

## 클래스: `Microscope_image_simulator`

### 생성자

```python
Microscope_image_simulator()
```

기본 광학 파라미터(NA=0.8, 단색 0.5876μm)로 초기화됩니다. `set_parameters()`를 내부적으로 호출합니다.

---

## 속성

### 광학 파라미터

| 속성 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `microscope_id` | `str` | `'OTF_0.8NA_'` | 현미경 식별자. 파일 저장 시 prefix |
| `NA` | `float` | `0.8` | 개구수 (Numerical Aperture). 동공 함수의 반지름 결정 |
| `wvls` | `list[float]` | `[0.5876]` | 파장 목록 (μm). He-d 스펙트럼 라인 기본값 |
| `mask_sampling_width_in_um` | `float` | `0.05` | 입력 마스크의 픽셀 크기 (μm/px). 주파수 격자 계산의 기준 |
| `custom_spectrum` | `bool` | `False` | 커스텀 스펙트럼 사용 여부 |
| `custom_image_property` | `bool` | `False` | 커스텀 이미지 속성 사용 여부 |

### 이미지/결과 속성

| 속성 | 타입 | 초기값 | 설명 |
|---|---|---|---|
| `H` | `int` | `1` | 로드된 이미지 높이 (px) |
| `W` | `int` | `1` | 로드된 이미지 너비 (px) |
| `mask_bmp` | `ndarray` or `None` | `None` | 로드된 그레이스케일 이미지 (float32) |
| `eff_OTF` | `ndarray` (complex) | — | 유효 다색 OTF (정규화됨) |
| `eff_OTF_uint` | `ndarray` or `None` | `None` | OTF 시각화용 이미지 (uint8, 0-255) |
| `imaged_gt_uint` | `ndarray` or `None` | `None` | 시뮬레이션 결과 이미지 (uint8, 0-255) |

### 주파수 도메인 속성 (`initialize_optics()` 이후)

| 속성 | 타입 | 설명 |
|---|---|---|
| `dkx` | `float` | x방향 주파수 샘플링 간격 (cycles/μm) |
| `dky` | `float` | y방향 주파수 샘플링 간격 (cycles/μm) |
| `RHO` | `ndarray` | 방사형 공간주파수 격자 `√(KX² + KY²)` (cycles/μm) |

---

## 메서드

### `set_parameters()`

기본 광학 파라미터를 설정/재설정합니다.

**파라미터:** 없음

**반환값:** 없음

**설정 값:** NA=0.8, wvls=[0.5876], mask_sampling_width_in_um=0.05

---

### `load_image(path)`

그레이스케일 BMP 이미지를 로드합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `path` | `str` | BMP 이미지 파일 경로 |

**반환값:** 없음

**설정되는 속성:**

| 속성 | 설명 |
|---|---|
| `mask_bmp` | `float32`로 변환된 이미지 배열 |
| `H`, `W` | 이미지 높이, 너비 |

---

### `load_grating_parameters(path)`

Tab 1에서 저장된 격자 파라미터 JSON에서 샘플링 정보를 읽습니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `path` | `str` | JSON 파일 경로 (Tab 1의 `grating_parameters.json`) |

**반환값:** 없음

**읽어오는 키:** `mask_sampling_width_in_um`

---

### `initialize_optics()`

주파수 도메인 격자를 구축합니다. 이미지 크기와 샘플링 정보를 기반으로 공간주파수 좌표계를 생성합니다.

**파라미터:** 없음

**반환값:** 없음

**사전 조건:** `load_image()` 및 `load_grating_parameters()` 호출 완료

**수식:**

주파수 샘플링 간격:
```
dkx = 1 / (W × mask_sampling_width_in_um)    [cycles/μm]
dky = 1 / (H × mask_sampling_width_in_um)    [cycles/μm]
```

주파수 격자:
```
kx = [0, dkx, 2×dkx, ...] - max/2    (중심이 0이 되도록)
ky = [0, dky, 2×dky, ...] - max/2
KX, KY = meshgrid(kx, ky)
RHO = √(KX² + KY²)
```

**설정되는 속성:** `dkx`, `dky`, `RHO`

---

### `check_simulation_condition()`

시뮬레이션 유효성을 검증합니다. 컷오프 주파수와 Nyquist 조건을 확인합니다.

**파라미터:** 없음

**반환값:** 없음 (실패 시 `AssertionError`)

**검증 조건:**

1. **상한 검사**: `NA / λ_min < max(RHO) / 5`
   - 컷오프 주파수가 주파수 도메인 최댓값의 1/5 미만이어야 함
   - OTF의 자기상관 특성상 컷오프의 2배까지 에너지가 퍼지므로 충분한 여유 필요
   - 위반 시: NA가 너무 크거나 입력 이미지의 샘플링이 너무 작음

2. **하한 검사**: `NA / λ_max > min(dkx, dky) × 4`
   - 컷오프 주파수가 주파수 샘플링 간격의 4배 이상이어야 OTF 형태 해상
   - 위반 시: NA가 너무 작거나 입력 이미지의 샘플링이 너무 큼

---

### `calculate_OTF()`

다색(polychromatic) 유효 OTF를 계산합니다.

**파라미터:** 없음

**반환값:** 없음

**사전 조건:** `initialize_optics()` 호출 완료

**알고리즘:**

각 파장 `λ`에 대해:
1. 컷오프 주파수 계산: `cf = NA / λ`
2. 원형 동공 함수 생성: `pupil(RHO) = 1 if RHO ≤ cf, else 0`
3. PSF 계산: `PSF = |iFFT(pupil)|²` (비간섭 이미징)
4. OTF 계산: `OTF = FFT(PSF)` (자기상관 정리에 의해 동공의 자기상관)

다색 합성:
```
eff_OTF = Σ OTF(λ_i) / Σ|eff_OTF|    (에너지 정규화)
```

**설정되는 속성:**

| 속성 | 타입 | 설명 |
|---|---|---|
| `eff_OTF` | `ndarray` (complex) | 정규화된 유효 OTF |
| `eff_OTF_uint` | `ndarray` (uint8) | OTF magnitude 시각화 이미지 (0-255) |

---

### `perform_OTF()`

로드된 이미지에 OTF를 적용하여 현미경 이미지를 시뮬레이션합니다.

**파라미터:** 없음

**반환값:** 없음

**사전 조건:** `calculate_OTF()` 호출 완료

**수식:**
```
result = |FFT(iFFT(input) × eff_OTF)|
```

이는 주파수 도메인에서의 곱셈 → 공간 도메인 컨볼루션과 동일합니다.

**설정되는 속성:**

| 속성 | 타입 | 설명 |
|---|---|---|
| `imaged_gt_uint` | `ndarray` (uint8) | 시뮬레이션 결과 (0-255 정규화) |

---

### `save_image(path=None, output_dir=None)`

결과 이미지를 BMP 파일로 저장합니다.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `path` | `str` or `None` | `None` | 저장 경로. `None`이면 `{microscope_id}microscope_image.bmp` |
| `output_dir` | `str` or `None` | `None` | 저장 디렉토리. 지정 시 파일명만 추출하여 해당 폴더에 저장 |

**반환값:** 없음

---

### `get_OTF()`

OTF 시각화 이미지를 반환합니다.

**파라미터:** 없음

**반환값:**

| 타입 | 설명 |
|---|---|
| `ndarray` (uint8) | `eff_OTF_uint` — OTF magnitude의 uint8 이미지 |

---

### `get_imaged_gt()`

시뮬레이션 결과 이미지를 반환합니다.

**파라미터:** 없음

**반환값:**

| 타입 | 설명 |
|---|---|
| `ndarray` (uint8) | `imaged_gt_uint` — 현미경 시뮬레이션 결과 이미지 |

---

### `run(bmp_path, json_path)`

전체 현미경 시뮬레이션 파이프라인을 실행합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `bmp_path` | `str` | 입력 격자 BMP 이미지 경로 |
| `json_path` | `str` | 격자 파라미터 JSON 경로 |

**반환값:** 없음

**실행 순서:**
1. `load_image(bmp_path)`
2. `load_grating_parameters(json_path)`
3. `set_parameters()` — 기본값 재설정
4. `initialize_optics()` — 주파수 격자 구축
5. `check_simulation_condition()` — 유효성 검증
6. `calculate_OTF()` — OTF 계산
7. `perform_OTF()` — 이미지에 OTF 적용
8. `save_image()` — 결과 저장

**사용 예시:**
```python
mis = Microscope_image_simulator()
mis.NA = 0.5
mis.run('grating.bmp', 'grating_parameters.json')
result = mis.get_imaged_gt()  # uint8 결과 이미지
```

---

## GUI 조작 순서

1. **Load Image** → 격자 BMP 파일 선택
2. **Load Parameters** → 격자 파라미터 JSON 로드 (sampling width 획득)
3. **NA 설정** → 좌측 패널에서 NA 값 입력
4. **Calculate OTF** → OTF 계산 및 GroupBox에 표시
5. **Generate Image** → 시뮬레이션 실행, 결과 이미지 표시

## 출력 파일

| 파일 | 설명 |
|---|---|
| `{microscope_id}microscope_image.bmp` | 현미경 시뮬레이션 결과 (uint8 그레이스케일) |

---

## 이론적 배경

### OTF와 비간섭 이미징

비간섭(incoherent) 이미징 시스템에서:
- **PSF** (Point Spread Function) = |FT⁻¹(Pupil)|²
- **OTF** (Optical Transfer Function) = FT(PSF) = Pupil ⊛ Pupil (자기상관)
- **이미지** = Object ⊗ PSF = FT⁻¹(FT(Object) × OTF)

컷오프 주파수: `f_cutoff = NA / λ` (cycles/μm)

OTF 대역폭 = 2 × f_cutoff (자기상관에 의한 대역 확장)
