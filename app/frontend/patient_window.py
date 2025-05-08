import sys

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QStringListModel

from frontend.base_window import BaseWindow
from frontend.utils.autocomplete import AutoComplete

class PatientWindow(BaseWindow):
    '''
    BaseWindow inherited class to display and handle the logic for the patient window.
    
    Methods:
        None
    '''
    
    def __init__(self, ui_file, coordinator, patient_manager):
        '''loads the vitals .ui file'''
        super().__init__(ui_file)
        self._coordinator = coordinator
        self._patient_manager = patient_manager
    
        self.search_patient.clicked.connect(self._search_patient)
        self._setup_autocomplete()


    def _update_ui(self):
        '''update the designated widjets when the current patient is changed'''
        if self.patient_state.current_patient is None:
            return
                
        current_patient = self.patient_state.current_patient

        # set the values of the widjets (all found within the .ui file)
        self.mrn_value.setText(current_patient.patient_mrn or '')
        self.lastname_value.setText(current_patient.lastname or '')
        self.firstname_value.setText(current_patient.firstname or '')
        self.gender_dropdown.setCurrentText(current_patient.gender or '')
        self.dob_value.setDate(current_patient.dob or '')
        self.weight_value.setText(str(current_patient.weight_kg) or 0.0)
        self.height_value.setText(str(current_patient.height_cm) or 0.0)


    def _search_patient(self):
        '''Searches a patient based on the inputted MRN'''
        mrn = self.mrn_value.text()

        if not mrn:
            self._handle_search_resposne(False)
            return

        # update the current patient state
        patient = self._coordinator.get_or_create_patient(mrn)
        if patient:
            self.patient_state.current_patient = patient

        self._handle_search_resposne(bool(patient))
        self._setup_autocomplete() # reload the autocomplete options


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


    def _setup_autocomplete(self):
        '''Sets up the autocomplete for the MRN input field'''
        
        # get a list of all patient then format the strings for the autocomplete
        patients = self._patient_manager.get_all_patients()
        options = [f"{patient.firstname} {patient.lastname} - {patient.patient_mrn}" for patient in patients]

        completer = AutoComplete(patients, options, self._patient_manager)
        completer.setModel(QStringListModel(options))
        self.mrn_value.setCompleter(completer)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("macOS")
    window = PatientWindow()
    window.show()
    sys.exit(app.exec())