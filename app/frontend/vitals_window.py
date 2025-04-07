import sys

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer, QDateTime, pyqtSlot

from frontend.base_window import BaseWindow
from frontend.utils.popup import PopupForm

from backend.managers.fluid_manager import FluidManager
from backend.managers.vitals_manager import VitalsManager
from backend.managers.ml_manager import MLManager

class VitalsWindow(BaseWindow):
    '''
    BaseWindow inherited class to display and handle the logic for the vitals window.
    '''

    def __init__(self, ui_file):
        '''Constructor for the VitalsWindow class, loads the vitals .ui file'''
        # pass the filepath for the vitals window ui file into the BaseWindow for displaying
        super().__init__(ui_file)

        # initalize backend managers
        self._fluid_manager = FluidManager()
        self._vitals_manager = VitalsManager()
        self._ml_manager = MLManager(model_type='xgb', binary=False, max_cache_size=100)
        self._ml_manager.load_model()

        # used to better represent the open/close state of the popup and precent duplicates
        self.popup = None
        self._pp_max = None
        self._pp_min = None

        # connect pyqt signals 
        # self._vitals_manager.vitals_data.connect(self._update_vitals)
        self.popup_button.clicked.connect(self._open_popup)
        
        # connect the pyqt signal for the ml manager to run the inference
        self._ml_manager.prediction_ready.connect(self._update_inference_fields)
        self.inference_button.clicked.connect(self._ml_manager.run_batched_inference)
        
        # setup ui components
        self._setup_units()
        self._setup_datetime()
        

    def _open_popup(self):
        '''Util funciton to open a popup and handle the logic/submission of the popup'''
        if not self.popup or not self.popup.isVisible():
            self.popup = PopupForm()
            self.popup.show()
            self.popup.form_submitted.connect(self._handle_popup_submission)


    def _handle_popup_submission(self, fluid, volume):
        '''Handle the logic for adding a record and display a popup to the user on success or fail'''
        if not self.patient_state.current_patient:
            QMessageBox.warning(
                self,
                "Error",
                "No patient selected. Please select a patient first."
            )
            return
        
        result = self._fluid_manager.add_record(self.patient_state.current_patient, fluid, volume)
        
        # display another popup for the user based on if the attemp was successful or not
        if result:
            self._update_ui()

            current_patient = f"{self.patient_state.current_patient.firstname} {self.patient_state.current_patient.lastname}"
            QMessageBox.information(
                self, 
                "Success", 
                f"Successfully recorded fluid administration for {current_patient}. \n\n Fluid: {fluid}\n Volume: {volume} mL"
            )
        else:
            QMessageBox.warning(
                self,
                "Error",
                "There was an issue recording the fluid administration. Please try again."
            )


    def _setup_units(self):
        '''setup the units for the textboxes'''
        units_mapping = {
            self.heart_rate_units: "bpm",
            self.spo2_units: "%",
            self.blood_pressure_units: "mmHg",
            self.map_units: "mmHg",
            self.rr_units: "bpm",
            self.ppv_units: "%",
            self.fluid_volume_units: "mL"
        }
        for widget, unit in units_mapping.items():
            widget.setText(f"<b>{unit}</b>")


    def _setup_datetime(self):
        '''setup the datetime widjet in the vitals window'''
        # Access the QDateTimeEdit widget
        self.current_datetime.setDisplayFormat("hh:mm:ss a MMM dd, yyyy")
        self.current_datetime.setDateTime(QDateTime.currentDateTime())
        self.current_datetime.setReadOnly(True)


        # Create and configure a QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_datetime)
        self.timer.start(1000)  # Update every 1 second


    def _update_datetime(self):
        '''update the datetime to display the current time'''
        # Update the QDateTimeEdit widget to the current date and time
        self.current_datetime.setDateTime(QDateTime.currentDateTime())


    def _update_ui(self):
        '''update the specific widjets when the current patient is changed'''
        if self.patient_state.current_patient is None:
            return

        current_patient = self.patient_state.current_patient
        self.name_value.setText(f"{current_patient.firstname} {current_patient.lastname}")
        self.mrn_value.setText(current_patient.patient_mrn)
        self.total_fluid_value.setText(str(self._fluid_manager.get_total_fluid_volume(current_patient) or ''))


    # I used a slot bc it supposedly increases memory efficieny and performance
    @pyqtSlot(dict)
    def _update_vitals(self, vitals_data):
        '''Update the vitals being shown on the page'''
        if not vitals_data:
            return
        
        # Update vital sign display values
        self.heart_rate_value.setText(str(vitals_data.get("heartRate", "")))
        self.map_value.setText(str(vitals_data.get("meanArterialPressure", "")))
        self.rr_value.setText(str(vitals_data.get("respiratoryRate", "")))
        self.blood_pressure_value.setText(f"{vitals_data.get('systolicBP', '')} / {vitals_data.get('diastolicBP', '')}")
        self.spo2_value.setText(str(vitals_data.get("spo2", "")))

        # Calculate and display pulse pressure variation
        ppv = self._calculate_ppv(
            vitals_data.get('systolicBP', ''), 
            vitals_data.get('diastolicBP', '')
        )
        self.ppv_value.setText(ppv)
        self._ml_manager.add_to_cache(vitals_data)


    def _update_inference_fields(self, prediction): 
        '''set the suggested actions based on the prediction made by the model'''
        self.volume_status_value.setText(prediction['label'])
        self.suggested_action_value.setText(prediction['suggested_action'])
        

    def _calculate_ppv(self, systolic, diastolic):
        '''calculates and returns the ppv of a patient'''
        # if there is no systolic or diastolic being sent, dont display anyting
        if not systolic or not diastolic:
            return ""
        
        # calculate the current pulse pressure
        current_pp = int(systolic) - int(diastolic)

        if self._pp_max is None or self._pp_min is None:
            # no ppv if it is the first reading, return zero and save the min and max
            self._pp_max = current_pp 
            self._pp_min = current_pp
            return "0.0"
        
        # Track max and min pp
        self._pp_max = max(self._pp_max, current_pp)
        self._pp_min = min(self._pp_min, current_pp)
        
        # if the denominator is 0, return 0 (stops division by 0 error)
        denominator = (self._pp_max + self._pp_min) / 2
        if denominator == 0:
            return "0.0"
        
        # calculate the variation in the pp and update the prev pp 
        ppv = ((self._pp_max - self._pp_min) / denominator) * 100

        return str(round(ppv, 1))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VitalsWindow()
    window.show()
    sys.exit(app.exec())