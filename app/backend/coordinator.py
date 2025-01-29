from backend.managers.fluid_manager import FluidManager
from backend.managers.patient_manager import PatientManager
from backend.managers.api_manager import EpicAPIManager

class BackendCoordinator:
    def __init__(self):
        self._fluid_manager = FluidManager()
        self._api = EpicAPIManager()
        self._patient_manager = PatientManager()

    