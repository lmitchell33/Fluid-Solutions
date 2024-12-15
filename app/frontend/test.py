import sys
from PyQt6 import QtWidgets, uic
from app.app import db_session
from database_models import Patient
from utils.db_utils import session_context, session_wrapper

def main():
    # Create the application
    app = QtWidgets.QApplication(sys.argv)
    
    # Load the UI file
    ui_file = "vitalsWindowV2.ui"  # Replace with the correct path to your UI file
    window = uic.loadUi(ui_file)
    
    # Apply the QSS stylesheet
    qss_styles = """
    QWidget {
        background-color: #f7f7f7;
        font-family: Arial, sans-serif;
        font-size: 14px;
        color: #333;
    }

    QLabel {
        color: #555;
        font-weight: bold;
    }

    QLineEdit, QComboBox, QSpinBox {
        background-color: #fff;
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 4px;
    }

    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        font-size: 14px;
    }

    QPushButton:hover {
        background-color: #45a049;
    }

    QPushButton:pressed {
        background-color: #3e8e41;
    }

    QGroupBox {
        border: 1px solid #ccc;
        border-radius: 8px;
        margin-top: 20px;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 4px;
        background-color: #f7f7f7;
    }
    """
    # app.setStyleSheet(qss_styles)
    
    # Show the window
    window.show()
    
    # Run the application
    sys.exit(app.exec())

@session_wrapper
def test():
    me = Patient(firstname="Lucas", lastname="Mitchell")
    db_session.add(me)


if __name__ == "__main__":
    test()
    # main()
