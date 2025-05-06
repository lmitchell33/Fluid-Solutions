from threading import Lock

from PyQt6.QtCore import QObject, pyqtSignal

from database_models import Patient

class PatientState(QObject):
    '''Singleton calss for managing the current Patient being displayed on the 
    application.
    
    This class implements a Singleton pattern because there will only ever be 
    one patient being shown on the screen. Furthermore, a threadsafe singleton
    pattern ensures consistency across all views/windows of the application. 
    By basing each view off of the singular instance of this class, the patient
    and its data will easily persist across each view. The alternative is a 
    property in the BaseWindow class, however, this was redundant and had
    unnecessary overhead. 

    I got this idea from the concept of states in React.

    Methods:
        get_current_patient() - returns the current patient
        set_current_patient(new_patient) - updates the current patient
    '''
    patient_changed = pyqtSignal()

    _instance = None
    _lock = Lock() # ensure thread safety
    
    def __new__(cls):
        '''Called before the __init__ method. Uses a Singleton pattern similar
        to the DatabaseManager class.
        '''
        if not cls._instance:
            with cls._lock:
                cls._instance = super(PatientState, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance
    

    def __init__(self):
        '''Constructor for the PatientState class'''
        # skip if instance of the class already exists
        if self._initialized:
            return 
        
        super().__init__()
        self._current_patient = None
        self._initialized  = True
    

    @property
    def current_patient(self):
        '''Getter for the current patient'''
        return self._current_patient
        

    @current_patient.setter
    def current_patient(self, new_patient: Patient):
        '''Setter for the current patient. Calls the _notify_observers func
        when the new patient is set, which updates the observer windows
        '''
        self._current_patient = new_patient
        self.patient_changed.emit() # emit the changes to all connected func's