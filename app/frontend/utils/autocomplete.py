from PyQt6.QtWidgets import QCompleter, QListView
from PyQt6.QtCore import Qt

class AutoComplete(QCompleter):
    def __init__(self, patients, options, patient_manager):
        super().__init__()
    
        self.setFilterMode(Qt.MatchFlag.MatchContains)
        self.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setPopup(QListView())
        self.popup().setMinimumHeight(200)
        self.setMaxVisibleItems(5) 

        self._patient_manager = patient_manager

        self.options_map = {option: patient.patient_mrn for option, patient in zip(options, patients)}


    def pathFromIndex(self, index):
        '''
        Override the pathFromIndex method to allow users to serach by typing
        a patients name or MRN, and always return the MRN of the patient for
        searching purposes.
        '''
        completion = super().pathFromIndex(index)

        if completion in self.options_map.keys():
            # return the mrn instead of the name
            return self.options_map.get(completion, completion)