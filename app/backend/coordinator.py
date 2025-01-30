from backend.managers.fluid_manager import FluidManager
from backend.managers.patient_manager import PatientManager
from backend.managers.api_manager import EpicAPIManager

class Coordinator:
    '''Coordinator class used to centralize workflows that involve multiple 
    classes in the frontend This is not meant to repalce business logic or the
    managers themselves.
    
    NOTE: Consider making this class a singleton.

    Methods:
        pass
    '''

    def __init__(self):
        self._fluid_manager = FluidManager()
        self._api = EpicAPIManager()
        self._patient_manager = PatientManager()

    
    def get_or_create_patient(self, patient_mrn):
        '''Return or create and return a patient isntance based on the inputted mrn'''
        patient = self._patient_manager.get_pateint_by_mrn(patient_mrn)
        if patient:
            return patient
        
        else:
            raw_patient_data = self._api.search_patient(_id=patient_mrn)
            return self._patient_manager.create_patient_from_epic(raw_patient_data)
        

    def remove_inactive_patients(self):
        """Removes inactive patients from the database based on API response."""
        patients = self._patient_manager.get_all_patients()
        
        # if there are no patients, dont do anything
        if not patients:
            print("No patients to remove")
            return

        # find the inactive patietns
        inactive_patients = self._api.get_inactive_patients(patients)

        # handle errors
        if not inactive_patients:
            print("No inactive patients to remove")
            return
        
        self._patient_manager.delete_patient(inactive_patients)


if __name__ == "__main__":
    coordinator = Coordinator()