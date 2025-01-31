import sys
from PyQt6.QtWidgets import QApplication

from frontend.base_window import BaseWindow

class PatientWindow(BaseWindow):
    '''
    BaseWindow inherited class to display and handle the logic for the patient window.
    
    Methods:
        None
    '''
    
    def __init__(self):
        '''Constructor for the PatientWindow class, loads the vitals .ui file'''
        super().__init__("frontend/views/patientWindow.ui")
    

    def _update_ui(self):
        if self.patient_state.current_patient is None:
            return
                
        # TODO: Add code to update the ui features when the current patient is changed.


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("macOS")
    window = PatientWindow()
    window.show()
    sys.exit(app.exec())