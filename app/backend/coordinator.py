class Coordinator:
    '''Coordinator class used to centralize workflows that involve multiple 
    classes in the frontend This is not meant to repalce business logic or the
    managers themselves.

    Methods:
        pass
    '''

    def __init__(self, fluid_manager, api_manager, patient_manager):
        self._fluid_manager = fluid_manager
        self._api = api_manager
        self._patient_manager = patient_manager

    
    def get_or_create_patient(self, patient_mrn):
        '''Return or create and return a patient isntance based on the inputted mrn'''
        # if the patient is found in the db, return the instance found
        if (patient := self._patient_manager.get_patient_by_mrn(patient_mrn)):
            return patient

        # if no patient is found in the external search return None 
        if not (raw_patient_data := self._api.search_patient(_id=patient_mrn)):
            return None

        # if a patient was found in the external search, add it to the database and return the new patient obj
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

        if not inactive_patients:
            print("No inactive patients to remove")
            return
        
        self._patient_manager.delete_patient(inactive_patients)


if __name__ == "__main__":
    coordinator = Coordinator()