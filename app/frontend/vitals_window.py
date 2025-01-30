import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QDateTime

from frontend.base_window import BaseWindow
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

        # self._populate_combo_box()
        self._setup_datetime()
        

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


    # def _populate_combo_box(self):
    #     '''Automatically populate the list of fluid names with those stored in the db'''
    #     fluids_dropdown = self.fluids_dropdown
    #     fluid_names = self._fluid_manager.get_all_fluid_names()
    #     fluids_dropdown.addItems(fluid_names)


    def _update_ui(self):
        if self.patient_state.current_patient is None:
            return

        # add code to update the features of the ui here 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VitalsWindow()
    window.show()
    sys.exit(app.exec())