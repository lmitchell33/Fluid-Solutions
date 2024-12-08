import sys
from PyQt6.QtWidgets import QApplication
from frontend.base_window import BaseWindow

class VitalsWindow(BaseWindow):
    '''
    BaseWindow inherited class to display and handle the logic for the vitals window.

    Methods:
        get_patient_routing_button(): returns the pyqt button obj for routing to the patient window
    '''

    def __init__(self):
        '''Constructor for the VitalsWindow class, loads the vitals .ui file'''
        # pass the filepath for the vitals window ui file into the BaseWindow for displaying
        super().__init__("frontend/views/vitalsWindowV2.ui")

    def get_patient_routing_button(self):
        ''' getter function to find and return the button obj to routing to the patient window
        Args:
            None

        Returns:
            button {obj} -- pyqt6 button object used for routing to the patient window
        '''
        
        return self.patient_window_button

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VitalsWindow()
    window.show()
    sys.exit(app.exec())