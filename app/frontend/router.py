from PyQt6.QtWidgets import QStackedWidget

from frontend.patient_window import PatientWindow
from frontend.vitals_window import VitalsWindow

from utils.db_utils import session_context
from database_models import Patient

class Router(QStackedWidget):
    """
    A class to manage routing between multiple windows in the application.
    
    NOTE: A stacked widget was chosen becuase it loads all views into memory when initalized
    making the switching of the views more efficent because of less load time. 
    However, if the model inference or SQLAlchemy uses too much RAM change this to a more
    simple routing method where you simply show and hide the windows, that way the number of 
    views loaded into memroy at once is limited to 1.
    
    It initializes and handles interactions between `PatientWindow` and `VitalsWindow`.

    Methods:
        show_window(window): Switches the displayed window to the specified one.
    """

    def __init__(self):
        '''Constructor for the Router, creates and adds all windows to the QStackedWidget.
        Also sets up the button click connections to handle the physical routing between the windows
        '''
        super().__init__()

        # initalize all windows
        self.patient_window = PatientWindow()
        self.vitals_window = VitalsWindow()

        # add the windows to the stakc
        self.addWidget(self.patient_window)
        self.addWidget(self.vitals_window)

        # set the inital (default) window 
        self.setCurrentWidget(self.patient_window)

        # NOTE: If any other windows are added, add the routing here
        self.vitals_window.get_patient_routing_button().clicked.connect(lambda: self.show_window(self.patient_window))
        self.patient_window.get_vitals_routing_button().clicked.connect(lambda: self.show_window(self.vitals_window))


    def show_window(self, window):
        ''' Sets the current window being shown to the specified window
        Args:
            window {QWidget or QMainWindow} -- The window to be currently displayed
            
        Returns:
            None
        '''
        self.setCurrentWidget(window)