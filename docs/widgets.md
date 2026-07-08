# UI 위젯 레퍼런스

**소스 파일**: `grating_simulator/ui/widgets.py`

## 개요

애플리케이션 전체에서 사용되는 커스텀 Qt 위젯들을 정의합니다. 비동기 작업 실행 및 진행률 표시, matplotlib figure 표시, 이미지 줌/팬, stdout 리디렉션 기능을 제공합니다.

---

## 클래스: `CancellationError`

**상속:** `Exception`

비동기 작업이 사용자에 의해 취소되었을 때 발생하는 예외입니다.
`WorkerThread` 내부에서 `progress_callback` 호출 시 취소 플래그가 설정되어 있으면 이 예외가 raise되어 작업 루프를 즉시 탈출합니다.

**파라미터:** 없음 (표준 `Exception` 동일)

**사용 위치:** `WorkerThread.make_callback()` 내부에서 자동으로 raise됨. 직접 사용할 필요 없음.

---

## 클래스: `WorkerThread`

**상속:** `QThread`

장시간 실행되는 함수를 별도 스레드에서 실행하고, 진행률/완료/에러/취소 시그널을 메인 스레드로 전달하는 워커입니다.

### 시그널

| 시그널 | 타입 | 설명 |
|---|---|---|
| `progress` | `Signal(int, int, str)` | 진행률 업데이트. `(current, total, message)` |
| `finished` | `Signal(object)` | 작업 정상 완료. 결과 객체를 전달 |
| `error` | `Signal(str)` | 작업 중 예외 발생. 포맷된 traceback 문자열을 전달 |
| `cancelled` | `Signal()` | 사용자 취소로 작업이 중단됨 |

### 생성자

```python
WorkerThread(fn, parent=None)
```

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `fn` | `callable` | (필수) | 실행할 함수. `fn(progress_callback=callback)` 형태로 호출됨 |
| `parent` | `QObject` or `None` | `None` | 부모 객체 (Qt 메모리 관리용) |

**내부 속성:**

| 속성 | 타입 | 설명 |
|---|---|---|
| `_fn` | `callable` | 실행할 함수 |
| `_cancelled` | `bool` | 취소 플래그. 초기값 `False` |

---

### `cancel()`

취소 플래그를 설정합니다. 다음 `progress_callback` 호출 시 `CancellationError`가 발생합니다.

**파라미터:** 없음

**반환값:** 없음

---

### `make_callback()`

작업 함수에 전달할 progress callback 클로저를 생성합니다.

**파라미터:** 없음

**반환값:** `callable` — `callback(current, total, msg="")` 형태의 함수

**콜백 동작:**

1. `_cancelled` 플래그 확인 → `True`이면 `CancellationError` raise
2. `progress` 시그널 emit: `(current, total, msg)`

---

### `run()`

`QThread.run()` 오버라이드. 스레드 시작 시 자동 호출됩니다.

**동작:**

1. `self._fn(progress_callback=self.make_callback())`을 호출
2. 정상 완료 & 취소되지 않음 → `finished` 시그널 emit (결과 객체 전달)
3. `CancellationError` 발생 → `cancelled` 시그널 emit
4. 기타 예외 발생 → `error` 시그널 emit (traceback 문자열 전달)

---

## 클래스: `ProgressDialog`

**상속:** `QDialog`

작업 진행률을 표시하고 사용자 취소 버튼을 제공하는 모달 대화상자입니다.

### 생성자

```python
ProgressDialog(title, parent=None)
```

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `title` | `str` | (필수) | 대화상자 제목 |
| `parent` | `QWidget` or `None` | `None` | 부모 위젯 |

**초기 설정:**

| 설정 | 값 | 설명 |
|---|---|---|
| `modal` | `True` | 모달 대화상자 (뒤쪽 UI 조작 불가) |
| `WindowCloseButtonHint` | 제거됨 | X 버튼 비활성화 (취소 버튼으로만 종료) |
| `fixedWidth` | `450` | 고정 너비 |

**내부 위젯:**

| 속성 | 타입 | 설명 |
|---|---|---|
| `_label` | `QLabel` | 상태 메시지 ("Preparing..." 초기값) |
| `_bar` | `QProgressBar` | 진행률 바 (minimum=0) |
| `_cancel_btn` | `QPushButton` | "Force Stop" 버튼 |

---

### `update_progress(current, total, msg)`

진행률 바와 라벨을 업데이트합니다. `WorkerThread.progress` 시그널에 연결하여 사용합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `current` | `int` | 현재 진행 값 |
| `total` | `int` | 전체 값 (progress bar maximum으로 설정됨) |
| `msg` | `str` | 상태 메시지. 빈 문자열이면 라벨 변경 안 함 |

**반환값:** 없음

---

### `set_cancelling()`

취소 진행 중 상태로 UI를 전환합니다. 라벨을 "Cancelling... please wait"로, 버튼을 비활성화하고 텍스트를 "Stopping..."으로 변경합니다.

**파라미터:** 없음

**반환값:** 없음

---

## 클래스: `PopupWindow`

**상속:** `QDialog`

matplotlib figure를 팝업 창으로 표시하기 위한 대화상자입니다.

### 생성자

```python
PopupWindow(parent=None, width=1280, height=720)
```

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `parent` | `QWidget` or `None` | `None` | 부모 위젯 |
| `width` | `int` | `1280` | 초기 창 너비 (px). 기본값 = `1920 × 2/3` |
| `height` | `int` | `720` | 초기 창 높이 (px). 기본값 = `1080 × 2/3` |

**속성:**

| 속성 | 타입 | 설명 |
|---|---|---|
| `layout` | `QVBoxLayout` | 내부 레이아웃 (여백 0, 간격 0) |

---

### `display_matplotlib_fig(graphics_view, fig)`

matplotlib Figure를 PNG로 렌더링하여 QGraphicsView에 표시합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `graphics_view` | `QGraphicsView` | figure를 표시할 뷰 (`ZoomableGraphicsView` 권장) |
| `fig` | `matplotlib.Figure` | 표시할 matplotlib figure |

**반환값:** 없음

**내부 동작:**

1. Figure 크기를 PopupWindow 크기에 맞게 조정 (DPI=600, 4배 스케일)
2. `fig.tight_layout()` 적용
3. PNG 바이트로 렌더링 (`fig.savefig`, DPI=600)
4. OpenCV로 디코딩 → QImage (BGR888) → QPixmap
5. QGraphicsScene에 pixmap 추가
6. 초기 스케일 0.25 (고해상도 렌더링을 축소 표시)

**사용 예시:**
```python
popup = PopupWindow()
zgv = ZoomableGraphicsView()
popup.layout.addWidget(zgv)
popup.display_matplotlib_fig(zgv, fig)
popup.show()
```

---

## 클래스: `ZoomableGraphicsView`

**상속:** `QGraphicsView`

마우스 휠 줌과 드래그 팬을 지원하는 이미지 뷰어입니다.

### 생성자

```python
ZoomableGraphicsView(parent=None)
```

**파라미터:**

| 이름 | 타입 | 기본값 | 설명 |
|---|---|---|---|
| `parent` | `QWidget` or `None` | `None` | 부모 위젯 |

**초기 설정:**

| 설정 | 값 | 설명 |
|---|---|---|
| `TransformationAnchor` | `AnchorUnderMouse` | 줌 중심 = 마우스 위치 |
| `ResizeAnchor` | `AnchorUnderMouse` | 리사이즈 기준 = 마우스 위치 |
| `ScrollBarPolicy` | `AlwaysOff` (양축) | 스크롤바 숨김 |
| `DragMode` | `ScrollHandDrag` | 드래그로 팬 |
| `ViewportUpdateMode` | `FullViewportUpdate` | 전체 뷰포트 갱신 |
| `RenderHint` | Antialiasing + SmoothPixmapTransform | 부드러운 렌더링 |

---

### `wheelEvent(event)`

마우스 휠 이벤트를 처리하여 줌 인/아웃을 수행합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `event` | `QWheelEvent` | 마우스 휠 이벤트 |

**동작:**

| 입력 | 동작 | 줌 팩터 |
|---|---|---|
| 휠 위로 (angleDelta.y > 0) | 확대 | ×1.25 |
| 휠 아래로 (angleDelta.y < 0) | 축소 | ×0.8 (= 1/1.25) |

**줌 보정:** 줌 후 마우스 아래 씬 좌표가 변하지 않도록 translate로 보정합니다:
```python
oldPos = mapToScene(event.position())
self.scale(zoomFactor, zoomFactor)
newPos = mapToScene(event.position())
self.translate(newPos - oldPos)    # 위치 고정
```

---

## 클래스: `TextRedirector`

**상속:** `QObject`

`sys.stdout` / `sys.stderr`를 QTextEdit 위젯으로 리디렉션하는 어댑터입니다.
시그널-슬롯 메커니즘을 사용하여 워커 스레드에서의 `print()` 호출도 스레드 안전하게 처리합니다.

### 시그널

| 시그널 | 타입 | 설명 |
|---|---|---|
| `_append_signal` | `Signal(str)` | 텍스트 추가 요청. `write()`에서 emit되어 `_append_text()` 슬롯에 연결됨 |

### 생성자

```python
TextRedirector(text_widget)
```

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `text_widget` | `QTextEdit` | 출력을 표시할 텍스트 위젯 |

**내부 동작:**

1. `super().__init__()` 호출 (QObject 초기화)
2. `text_widget` 속성 저장
3. `_append_signal.connect(self._append_text)` — 시그널을 슬롯에 연결

---

### `write(string)`

텍스트 추가 시그널을 emit합니다. 위젯을 직접 조작하지 않으므로 **어떤 스레드에서든 안전하게 호출 가능**합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `string` | `str` | 출력할 문자열 |

**동작:** `self._append_signal.emit(string)` — 메인 스레드의 `_append_text()` 슬롯이 호출됨

---

### `_append_text(string)` (슬롯)

`_append_signal`에 연결된 슬롯. 실제 QTextEdit 위젯 조작을 수행합니다. Qt 시그널-슬롯 메커니즘에 의해 항상 메인 스레드에서 실행됩니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `string` | `str` | 추가할 문자열 |

**동작:** `moveCursor(End)` → `insertPlainText(string)` → `moveCursor(End)`

---

### `flush()`

no-op. Python의 file-like 인터페이스 호환을 위한 메서드입니다.

---

## 사용 패턴

### `run_with_progress` 패턴 (비동기 작업 실행)

장시간 실행되는 작업을 별도 스레드에서 실행하면서 진행률 대화상자를 표시하는 패턴입니다.
`WorkerThread`, `ProgressDialog`, `CancellationError` 세 클래스가 협력합니다.

```python
# app.py 내 GratingSimulatorApp 메서드

def run_with_progress(self, fn, title, on_finished=None):
    """비동기 작업 실행 인프라"""
    # 1. 모든 버튼 비활성화 (중복 실행 방지)
    for btn in self.findChildren(QPushButton):
        btn.setEnabled(False)

    # 2. ProgressDialog + WorkerThread 생성
    self._progress_dlg = ProgressDialog(title, self)
    self._worker = WorkerThread(fn, parent=self)

    # 3. 시그널 연결
    self._worker.progress.connect(self._progress_dlg.update_progress)
    self._worker.finished.connect(
        lambda result: self._on_task_finished(result, on_finished))
    self._worker.error.connect(self._on_task_error)
    self._worker.cancelled.connect(self._on_task_cancelled)
    self._progress_dlg._cancel_btn.clicked.connect(self._request_cancel)

    # 4. 실행
    self._worker.start()
    self._progress_dlg.show()
```

**작업 함수 작성 패턴:**

```python
def calculate_OTF(self):
    """OTF 계산 — 전형적인 사용 예시"""
    print("calculating OTF...")
    self.mis.initialize_optics()

    # task: progress_callback 인자를 받는 함수
    def task(progress_callback=None):
        self.mis.calculate_OTF(progress_callback=progress_callback)

    # on_done: 작업 완료 후 UI 업데이트 (result 인자 받음)
    def on_done(_):
        self.display_image(self.ui.OTF_view, self.mis.eff_OTF_uint, ...)
        print("\t-> OTF calculated.\n")

    self.run_with_progress(task, "Calculating OTF (Microscope)", on_done)
```

**실행 흐름:**

1. `run_with_progress(task, title, on_done)` 호출
2. 모든 `QPushButton` 비활성화 → `ProgressDialog` 표시
3. `WorkerThread`가 별도 스레드에서 `task(progress_callback=...)` 실행
4. 작업 내부에서 `progress_callback(current, total, msg)` 호출 → 진행률 바 업데이트
5. 완료 → `on_done(result)` 호출 / 취소 → 메시지 출력 / 에러 → traceback 출력
6. 버튼 복원, 대화상자 닫힘

---

### app.py에서의 기타 사용 패턴

```python
# 1. stdout/stderr 리디렉션 (스레드 안전)
sys.stdout = TextRedirector(self.ui.terminalTextEdit)
sys.stderr = TextRedirector(self.ui.terminalTextEdit)

# 2. 이미지 표시
def display_image(self, graphics_view, img):
    scene = QGraphicsScene()
    # numpy → QPixmap 변환 → scene.addPixmap
    graphics_view.setScene(scene)

# 3. matplotlib figure 팝업
popup = PopupWindow(self)
zgv = ZoomableGraphicsView()
popup.layout.addWidget(zgv)
popup.display_matplotlib_fig(zgv, fig)
popup.show()
```
