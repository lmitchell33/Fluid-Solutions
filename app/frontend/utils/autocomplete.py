from PyQt6.QtWidgets import QCompleter, QListView
from PyQt6.QtCore import Qt

class AutoComplete(QCompleter):
    def __init__(self, patients, options, parent=None):
        super().__init__()
    
        self.setFilterMode(Qt.MatchFlag.MatchContains)
        self.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setPopup(QListView())
        self.popup().setMinimumHeight(200)
        self.setMaxVisibleItems(5) 


        self.options_map = {option: patient.patient_mrn for option, patient in zip(options, patients)}


    def pathFromIndex(self, index):
        '''Override the pathFromIndex method to only put the mrn in the textbox'''
        completion = super().pathFromIndex(index)

        if completion in self.options_map.keys():
            # put either the mrn or the completion itself in the textbox
            return self.options_map.get(completion, completion)