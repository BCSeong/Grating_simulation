from io import BytesIO

from PySide6.QtWidgets import QDialog, QVBoxLayout, QGraphicsScene, QGraphicsView
from PySide6.QtGui import QImage, QPixmap, QWheelEvent, QPainter, QTextCursor
from PySide6.QtCore import Qt

import numpy as np
import cv2


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

class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.moveCursor(QTextCursor.End)
        self.text_widget.insertPlainText(string)
        self.text_widget.moveCursor(QTextCursor.End)

    def flush(self):
        pass
