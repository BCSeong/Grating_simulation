import traceback
from io import BytesIO

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QGraphicsScene, QGraphicsView,
                                QLabel, QProgressBar, QPushButton)
from PySide6.QtGui import QImage, QPixmap, QWheelEvent, QPainter, QTextCursor
from PySide6.QtCore import Qt, Signal, QThread, QObject

import numpy as np
import cv2


class CancellationError(Exception):
    pass


class WorkerThread(QThread):
    progress = Signal(int, int, str)
    finished = Signal(object)
    error = Signal(str)
    cancelled = Signal()

    def __init__(self, fn, parent=None):
        super().__init__(parent)
        self._fn = fn
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def make_callback(self):
        def callback(current, total, msg=""):
            if self._cancelled:
                raise CancellationError()
            self.progress.emit(current, total, msg)
        return callback

    def run(self):
        try:
            result = self._fn(progress_callback=self.make_callback())
            if not self._cancelled:
                self.finished.emit(result)
        except CancellationError:
            self.cancelled.emit()
        except Exception:
            self.error.emit(traceback.format_exc())


class ProgressDialog(QDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        self.setFixedWidth(450)

        layout = QVBoxLayout(self)
        self._label = QLabel("Preparing...")
        self._bar = QProgressBar()
        self._bar.setMinimum(0)
        self._cancel_btn = QPushButton("Force Stop")
        layout.addWidget(self._label)
        layout.addWidget(self._bar)
        layout.addWidget(self._cancel_btn)

    def update_progress(self, current, total, msg):
        self._bar.setMaximum(total)
        self._bar.setValue(current)
        if msg:
            self._label.setText(msg)

    def set_cancelling(self):
        self._label.setText("Cancelling... please wait")
        self._cancel_btn.setEnabled(False)
        self._cancel_btn.setText("Stopping...")


''' Usage:
self.popup_window = PopupWindow()
self.popup_window.layout.addWidget(self.ui.pop_ZGV)
self.popup_window.display_matplotlib_fig(self.ui.pop_ZGV, fig)
self.popup_window.show()
'''
class PopupWindow(QDialog):
    def __init__(self, parent=None, width=int(1920*2/3), height=int(1080*2/3)):
        super().__init__(parent)
        self.setWindowTitle("Popup Window")
        self.resize(width, height)

        # 중앙 정렬을 위한 레이아웃 설정
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)  # 여백 제거
        self.layout.setSpacing(0)  # 위젯 간 간격 제거

    def display_matplotlib_fig(self, graphics_view, fig):
        # figure 크기를 PopupWindow 크기에 맞게 조정
        dpi = 600
        width_inch = self.width() / dpi *4
        height_inch = self.height() / dpi *4
        fig.set_size_inches(width_inch, height_inch)

        # 여백 최소화
        fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
        fig.tight_layout()

        buf = BytesIO()
        fig.savefig(
            buf,
            format='png',
            #bbox_inches='tight',
            #pad_inches=0,
            dpi=dpi,
            transparent=True
        )
        buf.seek(0)

        png_bytes = np.frombuffer(buf.read(), dtype=np.uint8)
        img_cv = cv2.imdecode(png_bytes, cv2.IMREAD_COLOR)
        h, w, ch = img_cv.shape
        bytes_per_line = ch * w
        qimg = QImage(img_cv.data, w, h, bytes_per_line, QImage.Format.Format_BGR888)
        pix = QPixmap.fromImage(qimg)

        scene = QGraphicsScene(self)
        scene.addPixmap(pix)
        graphics_view.setScene(scene)
        graphics_view.setAlignment(Qt.AlignCenter)
        graphics_view.resetTransform()  # 초기화
        graphics_view.scale(0.25, 0.25)   # 축소

class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)

    def wheelEvent(self, event: QWheelEvent):
        # Zoom Factor
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        # Save the scene pos
        oldPos = self.mapToScene(event.position().toPoint())

        # Zoom
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.scale(zoomFactor, zoomFactor)

        # Get the new position
        newPos = self.mapToScene(event.position().toPoint())

        # Move scene to old position
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())

class TextRedirector(QObject):
    _append_signal = Signal(str)

    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        self._append_signal.connect(self._append_text)

    def _append_text(self, string):
        self.text_widget.moveCursor(QTextCursor.End)
        self.text_widget.insertPlainText(string)
        self.text_widget.moveCursor(QTextCursor.End)

    def write(self, string):
        self._append_signal.emit(string)

    def flush(self):
        pass
