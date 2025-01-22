from database_manager import DatabaseManager
from database_models import Patient, Fluid, FluidRecord

class FluidManager:
    '''Fluid Manager class used for managing everything involving fluids and 
    fluid records with the database.
    
    Methods:
        get_all_fluids(): Returns a list of names of all fluids found in the db
    '''
    
    def __init__(self):
        self._db = DatabaseManager()


    def get_fluid_names(self):
        '''Queries the database gets a list of all fluid names stored.

        Returns: 
            names {List[str]} -- names of all fluids stored in the db
        '''
        with self._db.session_context() as session:
            return session.query(Fluid.fluid_name).all()
