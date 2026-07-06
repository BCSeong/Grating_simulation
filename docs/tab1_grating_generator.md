# Tab 1: Grating Generator (격자 생성기)

**소스 파일**: `grating_simulator/simulators/grating.py`

## 개요

이진(binary) 격자 마스크를 생성하는 모듈입니다. 톱니파(sawtooth) 삼각파 기하학에 기반하여 패턴을 만들고, morphological closing 연산으로 모서리를 둥글게 처리할 수 있습니다. 생성된 마스크는 Tab 2 (현미경), Tab 4 (프로젝션)의 입력으로 사용됩니다.

---

## 클래스: `Grating_generator`

### 생성자

```python
Grating_generator()
```

인스턴스 생성 시 기본 격자 파라미터로 초기화됩니다. 모든 파라미터는 인스턴스 속성으로 직접 설정하거나 `init()` 메서드로 일괄 설정할 수 있습니다.

---

## 속성 (파라미터)

### 일반 파라미터

| 속성 | 타입 | 기본값 | GUI 위젯 | 설명 |
|---|---|---|---|---|
| `gt_id` | `str` | `'21um_EPI'` | `headerLineEdit` | 격자 식별자. 파일 저장 시 prefix로 사용 |
| `mask_sampling_width_in_um` | `float` | `0.05` | `samplingPixelSizeUmDoubleSpinBox` | 마스크 픽셀의 물리적 크기 (μm/px). 이 값이 모든 물리 단위 계산의 기준 |

### 격자 기하학 파라미터

| 속성 | 타입 | 기본값 | GUI 위젯 | 설명 |
|---|---|---|---|---|
| `period_pattern` | `float` | `20.8` | `periodOfPatternUmDoubleSpinBox` | 패턴 전체 주기 (μm). 측정값 기반으로 입력 |
| `amplitude_of_saw` | `float` | `5.2` | `heightOfSawtoothUmDoubleSpinBox` | 톱니파 삼각형 높이 (μm). 꼭지점에서 밑변 중심까지 수직 거리 |
| `period_of_saw` | `float` | `1.98` | `periodOfSawtoothUmDoubleSpinBox` | 톱니파 밑변 너비 (μm). 삼각형 밑변의 전체 폭 |
| `width_of_stem` | `float` | `3.78` | `widthOfStemUmDoubleSpinBox` | 줄기(stem) 너비 (μm). 패턴 중심의 수직 연결부 폭 |
| `offset_btw_pattern` | `float` | `6.62` | `offsetBtwLinesDoubleSpinBox` | 인접 패턴 간 간격 (μm) |
| `number_of_pattern` | `int` | `3` | `numOfLinesSpinBox` | 수직 반복 횟수 |
| `length_of_grating_in_um` | `float` | `20` | `lengthOfLineUmDoubleSpinBox` | 격자 수평 길이 (μm) |

### 라운딩 파라미터

| 속성 | 타입 | 기본값 | GUI 위젯 | 설명 |
|---|---|---|---|---|
| `mask_rounding` | `bool` | `True` | `methodComboBox` | morphological closing 적용 여부 |
| `round_size_px` | `str` or `None` | `'AUTO'` | `methodComboBox` | 라운딩 모드. `'AUTO'`: 자동 커널 크기 결정, `None`: 라운딩 없음, `'User'`: 사용자 지정 |
| `round_size_px_user` | `int` | `1` | `factorSpinBox` | `round_size_px='User'` 일 때 사용할 커널 크기 (px) |
| `diameter_of_edge_of_saw_in_um` | `float` | `0.4` | `diameterOfEdgeOfSawtoothUmDoubleSpinBox` | 톱니파 꼭지점 너비 (μm). 실제 격자의 꼭지점이 무한히 날카롭지 않으므로 유한한 폭을 설정 |

### 기타

| 속성 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `invert_result` | `bool` | `False` | `True`이면 최종 마스크를 반전 (흑백 교환) |

---

## 메서드

### `init(parameters)`

딕셔너리로 여러 속성을 한 번에 설정합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `parameters` | `dict` | `{속성명: 값}` 형태의 딕셔너리. 키는 클래스 속성 이름과 일치해야 함 |

**반환값:** 없음

**사용 예시:**
```python
gg = Grating_generator()
gg.init({'period_pattern': 25.0, 'invert_result': True})
```

---

### `check_parameter_consistency()`

입력 파라미터의 일관성을 검증합니다. 계산된 주기와 측정된 주기가 일치하는지 확인합니다.

**파라미터:** 없음

**반환값:** 없음 (내부 속성 `period_gen_sine` 설정)

**검증 수식:**

```
period_gen_sine = (amplitude_of_saw + width_of_stem/2 + offset_btw_pattern/2) × 2
```

이 값이 `period_pattern`과 1e-4 이내로 일치해야 합니다. 불일치 시 `AssertionError`를 발생시킵니다.

**설정되는 속성:**

| 속성 | 타입 | 설명 |
|---|---|---|
| `period_gen_sine` | `float` | 계산된 사인파 방향 주기 (μm) |

---

### `generate_grating()`

2D 이진 마스크를 생성합니다. 톱니파 삼각형 기하학으로 패턴 영역을 정의하고, morphological closing으로 모서리를 둥글게 처리합니다.

**파라미터:** 없음

**반환값:** 없음 (내부 속성 설정)

**사전 조건:** `check_parameter_consistency()` 호출 필요 (`period_gen_sine` 사용)

**알고리즘:**

1. 톱니파 기하학 파라미터 계산:
   ```
   a = amplitude_of_saw - diameter_of_edge_of_saw_in_um / 2
   b = period_of_saw
   c = diameter_of_edge_of_saw_in_um
   A = a × b / (b - c)    ← 이등변 삼각형 전체 높이
   ```

2. 삼각파 트레인(triangle train) 생성:
   ```
   f1(x) = A × |2 × (x/T - floor(x/T + 0.5))| + B1    ← 상한 경계
   f2(x) = A × |2 × (x/T - floor(x/T + 0.5))| + B2    ← 하한 경계
   ```
   여기서 `T = period_of_saw`, `B1 = width_of_stem / 2`, `B2 = -(A + B1)`

3. 마스크 생성: `f2 ≤ Y ≤ f1` 영역이 패턴 (값 1), 나머지가 배경 (값 0)

4. (선택) Morphological closing 적용:
   - 커널: `cv2.MORPH_ELLIPSE` (타원형)
   - `AUTO` 모드: 생성된 패턴 주기가 측정 주기와 일치할 때까지 커널 크기를 반복 조정

**설정되는 속성:**

| 속성 | 타입 | shape | 설명 |
|---|---|---|---|
| `mask_ori` | `ndarray[bool]` | `(H_single, W)` | 원본 이진 마스크 (라운딩 전, 1주기) |
| `mask_gen` | `ndarray[bool]` | `(H_single, W)` | 최종 이진 마스크 (라운딩 후, 1주기) |

**기하학 도식:**

```
▲ y축 (위로)
|         /|
|        / |
|       /  |
|      /   |
|     /----|   ← 선분 C (너비 c = diameter_of_edge_of_saw_in_um)
|    /     |
|   /      |
|  /       | a ← amplitude_of_saw - c/2
| /        |
|/---------|   ← 선분 B (너비 b = period_of_saw)
```

이등변 삼각형의 전체 높이: `A = a × b / (b - c)`

---

### `image_stacker()`

단일 주기 마스크를 수직으로 반복 적층하여 전체 격자 버퍼를 생성합니다.

**파라미터:** 없음

**반환값:** 없음 (내부 속성 설정)

**사전 조건:** `generate_grating()` 호출 필요 (`mask_gen` 사용)

**연산:** `buffer = vstack([mask_gen] × number_of_pattern)`

**설정되는 속성:**

| 속성 | 타입 | shape | 설명 |
|---|---|---|---|
| `buffer` | `ndarray[bool]` | `(H, W)` | 적층된 전체 격자 이미지. `H = H_single × number_of_pattern` |
| `H` | `int` | — | 최종 이미지 높이 (px) |
| `W` | `int` | — | 최종 이미지 너비 (px) |

---

### `invert_grating()`

모든 마스크의 흑백을 반전합니다 (bitwise NOT).

**파라미터:** 없음

**반환값:** 없음

**영향받는 속성:** `mask_ori`, `mask_gen`, `buffer`

---

### `save_grating(output_dir=None)`

격자 이미지를 BMP 파일로 저장합니다.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `output_dir` | `str` or `None` | `None` | 저장 디렉토리. `None`이면 현재 디렉토리 |

**반환값:** 없음

**저장 파일:**
- `{gt_id}grating_close({mask_rounding}).bmp` — 정상 마스크 (uint8, 0/255)
- `{gt_id}grating_close({mask_rounding})_rev.bmp` — 반전 마스크

---

### `matplot_grating()`

세 가지 마스크를 matplotlib으로 표시합니다: 원본(`mask_ori`), 라운딩 후(`mask_gen`), 적층(`buffer`).

**파라미터:** 없음

**반환값:** 없음 (`plt.show()` 호출)

---

### `run(display=False, save=False)`

전체 격자 생성 파이프라인을 실행합니다.

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `display` | `bool` | `False` | `True`이면 matplotlib으로 결과 표시 |
| `save` | `bool` | `False` | `True`이면 BMP 파일 저장 |

**반환값:** 없음

**실행 순서:**
1. `check_parameter_consistency()` — 파라미터 검증
2. `generate_grating()` — 마스크 생성
3. `image_stacker()` — 적층
4. (조건) `invert_grating()` — `invert_result=True`이면
5. (조건) `matplot_grating()` — `display=True`이면
6. (조건) `save_grating()` — `save=True`이면

**사용 예시:**

```python
gg = Grating_generator()
gg.period_pattern = 25.0
gg.amplitude_of_saw = 6.0
gg.run(display=True, save=True)

# 또는 init()으로 일괄 설정
gg2 = Grating_generator()
gg2.init({'period_pattern': 25.0, 'invert_result': True})
gg2.run()
```

---

## GUI 조작 순서

1. **파라미터 입력**: 좌측 패널에서 격자 기하학 값 설정
2. **Initialize** 버튼 → `check_parameter_consistency()` 실행, 계산/측정 주기 일치 확인
3. **Run** 버튼 → `generate_grating()` + `image_stacker()` 실행, 3개 GroupBox에 결과 표시
4. **Save** 버튼 → 세션 폴더에 BMP 저장

## 출력 파일

| 파일 | 설명 |
|---|---|
| `{gt_id}grating_close({rounding}).bmp` | 격자 마스크 (uint8, 0 또는 255) |
| `{gt_id}grating_close({rounding})_rev.bmp` | 반전 마스크 |
| `grating_parameters.json` | 파라미터 JSON (Tab 2/4에서 로드) |

---

## 파라미터 관계 다이어그램

```
period_pattern (전체 주기)
├── amplitude_of_saw × 2 (삼각형 높이 × 2)
├── width_of_stem (줄기 너비)
└── offset_btw_pattern (패턴 간격)

검증 조건: period_pattern = (amplitude_of_saw + width_of_stem/2 + offset_btw_pattern/2) × 2
```
