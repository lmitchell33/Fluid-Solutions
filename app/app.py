import sys
from PyQt6.QtWidgets import QApplication
from frontend.router import Router


def main():
    # starts the application from the cli and initalizes the router
    app = QApplication(sys.argv)
    router = Router()
    router.show() # NOTE: by default, this shows the patient window
    sys.exit(app.exec())


if __name__ == "__main__":
    main()