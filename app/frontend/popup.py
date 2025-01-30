import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import uic

class PopupForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("./frontend/views/popup.ui", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PopupForm()
    window.show()
    sys.exit(app.exec())