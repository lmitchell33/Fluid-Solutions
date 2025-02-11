from datetime import datetime

from database_manager import DatabaseManager
from database_models import Patient

class PatientManager:
    '''Patient Manager class used for managing new and old patient instances
    
    Methods:
        pass
    '''
    def __init__(self):
        self._db = DatabaseManager()


    def create_patient_from_epic(self, raw_patient_data):
        # the keys represent the result parameters from epic and the values
        # represent the attributes of the Patient Class
        epic_field_mapping = {
            "id" : "patient_mrn",
            "birthDate" : "dob",
            "family" : "lastname",
            "given" : "firstname",
            "gender" : "gender"
        }

        if not isinstance(raw_patient_data, dict):
            print("Invalid raw patient data")
            return None
        
        try:
            # create a mew patient and populate its attributes with the data from epic  
            with self._db.session_context() as db:
                new_patient = Patient()
                
                # add attributes to the patient instance
                for key, value in raw_patient_data.items():
                    if key in epic_field_mapping.keys():

                        # conver the date of birth to a date object for SQLAclhemy
                        if key == "birthDate" and value: 
                            value = datetime.strptime(value, "%Y-%m-%d").date()

                        setattr(new_patient, epic_field_mapping[key], value)

                db.add(new_patient)
                db.commit()

            return new_patient
        
        except Exception as e:
            print("Error creating patient isntance: ", e)
            return None

    
    def get_patient_by_mrn(self, mrn):
        '''Fetches the patient instance from the database based on the inputted MRN'''
        with self._db.session_context() as db:
            
            # if the patient instance from the db exists, put it into the patient variable and return 
            if (patient := db.query(Patient).filter_by(patient_mrn=mrn).first()):
                return patient
            
            return None


    def get_all_patients(self):
        '''Returns a list of patient instances'''
        with self._db.session_context() as db:
            return db.query(Patient).all()


    def get_all_patient_names(self):
        '''Returns the list of names of all patients currently stored in the database'''
        with self._db.session_context() as db:
            return [f"{patient.firstname or ''} {patient.lastname or ''}" for patient in db.query(Patient).all()]


    def delete_patient(self, patient):
        '''Delete the designated patient(s)'''
        with self._db.session_context() as db:
            if isinstance(patient, list):
                db.query(Patient).filter(Patient.id.in_([p.id for p in patient])).delete(synchronize_session=False)
            
            else:
                db.delete(patient)

            db.commit()


if __name__ == "__main__":
    pm = PatientManager()
