import sys

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer, QDateTime

from frontend.base_window import BaseWindow
from frontend.popup import PopupForm
from backend.managers.fluid_manager import FluidManager

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

        self._fluid_manager = FluidManager()

        self.popup = None

        self.popup_button.clicked.connect(self._open_popup)
        self._setup_datetime()
        

    def _open_popup(self):
        if not self.popup:
            self.popup = PopupForm()
            self.popup.form_submitted.connect(self._handle_popup_submission)
            self.popup.show()
            self.popup.destroyed.connect(self._close_popup)


    def _close_popup(self):
        self.popup = None


    def _handle_popup_submission(self, fluid, volume):
        result = self._fluid_manager.add_record(self.patient_state.current_patient, fluid, float(volume))
        
        if result:
            message = (f"Successfully recorded fluid administration for {self.patient_state.current_patient.firstname or ''} "
                f"{self.patient_state.current_patient.lastname or ''}.\n\n"
                f"Fluid: {fluid}\nVolume: {volume} mL")
            QMessageBox.information(self, "Success", message)
        else:
            message = "There was an issue recording the fluid administration. Please try again."
            QMessageBox.warning(self, "Error", message)


    def _setup_datetime(self):
        # Access the QDateTimeEdit widget
        self.current_datetime.setDisplayFormat("hh:mm:ss a MMM dd, yyyy")
        self.current_datetime.setDateTime(QDateTime.currentDateTime())
        self.current_datetime.setReadOnly(True)
        

        # Create and configure a QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._updateDateTime)
        self.timer.start(1000)  # Update every 1 second


    def _updateDateTime(self):
        # Update the QDateTimeEdit widget to the current date and time
        self.current_datetime.setDateTime(QDateTime.currentDateTime())


    def _update_ui(self):
        if self.patient_state.current_patient is None:
            return

        # add code to update the features of the ui here 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VitalsWindow()
    window.show()
    sys.exit(app.exec())