import sys
from PySide6.QtWidgets import QApplication
from grating_simulator.app import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
