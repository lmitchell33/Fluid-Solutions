from datetime import datetime

from database_manager import DatabaseManager
from database_models import Fluid, FluidRecord

class FluidManager:
    '''Fluid Manager class used for managing everything involving fluids and 
    fluid records with the database.
    
    Methods:
        get_all_fluids(): Returns a list of names of all fluids found in the db
    '''
    
    def __init__(self):
        self._db = DatabaseManager()


    def add_record(self, patient, fluid_name, amount_mL):
        with self._db.session_context() as session:
            fluid = session.query(Fluid).filter_by(fluid_name=fluid_name).first()

            new_record = FluidRecord(fluid_time_given=datetime.now(), amount_mL=amount_mL, fluid=fluid, patient=patient)

            fluid.fluid_records.append(new_record)
            patient.fluid_records.append(new_record)

        # TODO: replace this with some way of showing the user it was successful
        print("Successfully created fluid record")
        # return True

    def get_patient_records(self, patient, start_time=None, end_time=None):
        pass


    def get_fluid_volume(self, patient, start_time=None, end_time=None):
        pass


    def get_fluid_names(self):
        '''Queries the database gets a list of all fluid names stored.

        Returns: 
            names {List[str]} -- names of all fluids stored in the db
        '''
        with self._db.session_context() as session:
            return session.query(Fluid.fluid_name).all()


    def _create_record(self, patient, fluid_id, amount_ml, time_given):
        pass


    def _get_patient(self, patient):
        pass
