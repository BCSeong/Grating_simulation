# UI 위젯 레퍼런스

**소스 파일**: `grating_simulator/ui/widgets.py`

## 개요

애플리케이션 전체에서 사용되는 커스텀 Qt 위젯들을 정의합니다. matplotlib figure 표시, 이미지 줌/팬, stdout 리디렉션 기능을 제공합니다.

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

`sys.stdout` / `sys.stderr`를 QTextEdit 위젯으로 리디렉션하는 어댑터입니다.

### 생성자

```python
TextRedirector(text_widget)
```

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `text_widget` | `QTextEdit` | 출력을 표시할 텍스트 위젯 |

---

### `write(string)`

텍스트를 위젯에 추가하고 커서를 끝으로 이동합니다.

**파라미터:**

| 이름 | 타입 | 설명 |
|---|---|---|
| `string` | `str` | 출력할 문자열 |

**동작:** `moveCursor(End)` → `insertPlainText(string)` → `moveCursor(End)`

---

### `flush()`

no-op. Python의 file-like 인터페이스 호환을 위한 메서드입니다.

---

## 사용 패턴

### app.py에서의 전형적인 사용

```python
# 1. stdout/stderr 리디렉션
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
