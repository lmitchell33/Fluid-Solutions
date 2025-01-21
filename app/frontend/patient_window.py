import sys

from PyQt6.QtWidgets import QApplication
from frontend.base_window import BaseWindow

class PatientWindow(BaseWindow):
    '''
    BaseWindow inherited class to display and handle the logic for the patient window.
    '''
    
    def __init__(self):
        '''Constructor for the PatientWindow class, loads the vitals .ui file'''
        super().__init__("frontend/views/patientWindow.ui")
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PatientWindow()
    window.show()
    sys.exit(app.exec())