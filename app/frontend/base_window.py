from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

from backend.patient_state import PatientState

class BaseWindow(QMainWindow):
    '''
    Base class for creating windows from .ui files. All shared methods between all windows should
    go into this class

    Methods:
        get_routing_button(): finds and returns the routing button for the loaded window
    '''

    def __init__(self, ui_file):
        ''' Constructor for the BaseWindow class, loads the specified .ui file
        Args:
            ui_file {str} -- Filepath to the .ui file to load. These files should all be in the /frontend/views/ directory
            
            
        Returns:
            None 
        '''
        super().__init__()
        uic.loadUi(ui_file, self)
        self.routes_to = None

        # Initialize patient state used to display the current patient being shown
        self.patient_state = PatientState()
        self.patient_state.add_observer(self._on_patient_change)


    def get_routing_button(self):
        '''getter funciton to find and return the button obj from the xml'''

        return self.routing_button
    

    def _on_patient_change(self, new_patient):
        self._update_ui()


    def _update_ui(self):
        '''override this in each extended class'''
        pass