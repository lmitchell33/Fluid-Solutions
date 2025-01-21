import sys

from PyQt6.QtWidgets import QApplication
from frontend.base_window import BaseWindow

class PatientWindow(BaseWindow):
    '''
    BaseWindow inherited class to display and handle the logic for the patient window.

    Methods:
        get_vitals_routing_button(): returns the pyqt button obj for routing to the vitals window
    '''
    
    def __init__(self):
        '''Constructor for the PatientWindow class, loads the vitals .ui file'''
        super().__init__("frontend/views/patientWindow.ui")
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PatientWindow()
    window.show()
    sys.exit(app.exec())