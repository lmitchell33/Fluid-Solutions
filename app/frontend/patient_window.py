import sys
from PyQt6.QtWidgets import QApplication, QMessageBox

from frontend.base_window import BaseWindow
from backend.coordinator import Coordinator

class PatientWindow(BaseWindow):
    '''
    BaseWindow inherited class to display and handle the logic for the patient window.
    
    Methods:
        None
    '''
    
    def __init__(self):
        '''Constructor for the PatientWindow class, loads the vitals .ui file'''
        super().__init__("frontend/views/patientWindow.ui")
        self._coordinator = Coordinator()
    
        self.search_patient.clicked.connect(self._search_patient)


    def _update_ui(self):
        '''update the designated widjets when the current patient is changed'''
        if self.patient_state.current_patient is None:
            return
                
        current_patient = self.patient_state.current_patient

        # set the values of the widjets 
        self.mrn_value.setText(current_patient.patient_mrn or '')
        self.lastname_value.setText(current_patient.lastname or '')
        self.firstname_value.setText(current_patient.firstname or '')
        self.gender_dropdown.setCurrentText(current_patient.gender or '')
        self.dob_value.setDate(current_patient.dob or '')
        self.weight_value.setText(str(current_patient.weight_kg) or 0.0)
        self.height_value.setText(str(current_patient.height_cm) or 0.0)


    def _search_patient(self):
        '''Searches a patient based on the inputted MRN'''
        # TODO: Update the logic here based on what we would rather have,
        # right now it only searches based on MRN but I can add other parameters
        # The other parameters would be useful if the mrn is not known

        mrn = self.mrn_value.text()

        if not mrn:
            self._handle_search_resposne(False)
            return

        if patient := self._coordinator.get_or_create_patient(mrn):
            self.patient_state.current_patient = patient
            search_success = True
        else:
            search_success = False

        self._handle_search_resposne(search_success)


    def _handle_search_resposne(self, success):
        '''Handles the logic involved withthe response of seraching for patient'''
        if success:
            QMessageBox.information(
                self, 
                "Search Successful!", 
                f"Patient Found: {self.patient_state.current_patient.firstname} {self.patient_state.current_patient.lastname}"
            )
        else:
            QMessageBox.warning(
                self, 
                "Search Failed!", 
                "No patient found with the given MRN"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("macOS")
    window = PatientWindow()
    window.show()
    sys.exit(app.exec())