import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QDateTime

from frontend.base_window import BaseWindow

class VitalsWindow(BaseWindow):
    '''
    BaseWindow inherited class to display and handle the logic for the vitals window.
    
    Methods:
        None
    '''

    def __init__(self):
        '''Constructor for the VitalsWindow class, loads the vitals .ui file'''
        # pass the filepath for the vitals window ui file into the BaseWindow for displaying
        super().__init__("frontend/views/vitalsWindow.ui")

        # Access the QDateTimeEdit widget
        self.dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.dateTimeEdit.setReadOnly(True)


        # Create and configure a QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._updateDateTime)
        self.timer.start(1000)  # Update every 1 second

        

    def _updateDateTime(self):
        # Update the QDateTimeEdit widget to the current date and time
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())


    def _update_ui(self):
        if self.patient_state.current_patient is None:
            return

        # add code to update the features of the ui here 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VitalsWindow()
    window.show()
    sys.exit(app.exec())