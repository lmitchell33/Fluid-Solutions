from datetime import datetime

from database_models import Fluid, FluidRecord

class FluidManager:
    '''Fluid Manager class used for managing everything involving fluids and 
    fluid records with the database.
    
    Methods:
        get_all_fluids(): Returns a list of names of all fluids found in the db
        add_record(patient_id, fluid_name, amount_ml) - adds a fluidrecord to a patient
        get_total_fluid_volume(patient_id) - returns the total fluid volume administered to a patient
    '''
    def __init__(self, db_manager): 
        self._db = db_manager


    def add_record(self, patient, fluid_name, amount_ml):
        '''Adds a fluid record for a designated patient. If a inputted fluid 
        name is not found in the database, it will create a new fluid.
        
        Args: 
            patient {Patient} -- Patient instance to whom the fluid record belongs
            fluid_name {str} -- the name of the fluid being recorded
            amount_mL {float} -- The volume of fluid that was administered
        '''
        if not patient:
            return False
        
        if amount_ml == 0.0:
            return False
        
        try:
            with self._db.session_context() as db:
                fluid = db.query(Fluid).filter_by(name=fluid_name).first()
                
                # if the fluid is not found, create one
                if not fluid:
                    fluid = Fluid(name=fluid_name)
                    db.add(fluid)

                # create a new fluid record and assign it to the patient and fluid
                new_fluid_record = FluidRecord(fluid_time_given=datetime.now(), amount_ml=amount_ml, fluid=fluid, patient=patient)
                db.add(new_fluid_record)

                fluid.fluid_records.append(new_fluid_record)
                patient.fluid_records.append(new_fluid_record)

                db.commit()

                print("Successfully created fluid record")
                return True
        
        except Exception as e:
            print(f"Failed to create fluid record: {e}")
            return False


    def get_total_fluid_volume(self, patient, fluid=None):
        '''Calculates the total volume of fluid administered to a specific patient
        
        Args:
            patient {Patient} -- The unique db id of the patient for whom the total fluid volume is administered to
            fluid {str} -- Name of the specific fluid to query, default to None

        Returns:
            sum {int} -- total fluid volume (mL) administered to the patient    
        '''
        try:
            records = patient.fluid_records
            
            if fluid:
                records = [record for record in records if record.fluid.name == fluid]
                
            return sum([record.amount_ml for record in records])
                
        except Exception as e:
            print(f"Failed to get the total fluid volume {e}")


    def get_all_fluid_names(self):
        '''Queries the database gets a list of all fluid names stored.

        Returns: 
            names {List[str]} -- names of all fluids stored in the db
        '''
        with self._db.session_context() as db:
            return [fluid.name for fluid in db.query(Fluid).all()]