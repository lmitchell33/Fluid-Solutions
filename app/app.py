import sys
from PyQt6.QtCore import QFile, QTextStream
from PyQt6.QtWidgets import QApplication
from frontend.router import Router


def load_stylesheet(stylesheet):
    '''util function to load in a QSS stylesheet to apply to the app as a whole
    NOTE: This will apply to ALL windows in the app unless a stylesheet is applied directly to the other window
    Args:
        stylesheet {str} -- path to the .qss file containing the styling
    
    Returns:
        stream {QTextStream} -- PyQt obj containing the styling information needed to pass into QApplication.setStyleSheet()
    '''
    
    file = QFile(stylesheet)
    if file.open(QFile.OpenModeFlag.ReadOnly):
        stream = QTextStream(file)
        return stream.readAll()
    return ""


def main():
    # starts the application from the cli and initalizes the router
    app = QApplication(sys.argv)
    router = Router()
    app.setStyleSheet(load_stylesheet("frontend/stylesheets/window.qss"))
    router.show() # NOTE: by default, this shows the patient window
    sys.exit(app.exec())


if __name__ == "__main__":
    main()