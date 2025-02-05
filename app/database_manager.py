from contextlib import contextmanager
from threading import Lock
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from database_models import Fluid, Base, Patient

class DatabaseManager:
    '''Singleton class for managing database connections and sessions.
    
    This class implements a Singleton pattern, ensuring that only one instance
    of the `DatabaseManager` class exists throughout the application. It is 
    responsible for creating and managing the SQLAlchemy engine and session.
    The database is accessed via the `session_conext()` method, which hanldes
    the creation, commits, rollback, and closure of a session. The Singleton 
    is used here because pretty much all modules need to use DatabaseManager 
    databse connections are fairly expensive, therefore, only having one 
    instance of the class is ideal because there will only ever be one
    connection to the database. 

    The class provides methods to initalize the database schema with the 
    `initdb(Base)` method by dropping all tables and re-creating them.
    
    Methods:
        initdb(Base): Initializes the database by dropping and creating tables.
        session_context(): Context manager for safely handling database sessions, committing changes and rolling back on errors.
    '''
    _instance = None
    _lock = Lock() # thread lock to prevent race conditions

    def __new__(cls):
        '''Called before the __init__ method. This uses a Singleton pattern, 
        meaning only one instance of the DatabaseManager exists throughout
        the application. This maintains consistency and saves resources.

        Example:
            db1 = DatabaseManager()
            db2 = DatabaseManager()
            db3 = DatabaseManager()
            ^ These all point to the same instance

        Args:
            cls {class} - the class itself. The 'self' pointing to the class,
                          rather then to the instance.

        Returns:
            cls._instance {DatabaseManager} - the singular instance of the class.
        '''
        
        # If instance does not exist, then initalize an instance and set the 
        # initalized flag to ensure no more instances of the class be created.
        if not cls._instance:
            with cls._lock:
                if not cls._instance: 
                    # double check the locking
                    cls._instance = super(DatabaseManager, cls).__new__(cls)
                    cls._instance._initialized  = False
        
        return cls._instance

    def __init__(self, database_url="sqlite:///instance/data.db"):
        '''Constructor for the DatabaseManager class, creates the sqlite
        engine and a scoped session. Also sets the initalized flag, preventing
        mulitple instances of the class from being made
        
        Kwargs:
            database_url {string} - path/url for the sqlite database
        '''
        
        # if an instance of the class already exists, skip to save resources
        if self._initialized:
            return 
        
        self._initialized  = True

        self._database_url = database_url
        self._create_session()
        

    def initdb(self):
        '''initalizes the database by dropping all tables then re-creating the 
        the tables.

        Args:
            Base {sqlalchemy.ext.declarative.base} -- base class that holds all tables
        '''

        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        
        self._session.add(Patient(firstname="Jackson", lastname="Jewell", patient_mrn="1", gender="female", weight_kg=500.0, height_cm=100.0, dob=datetime.now().date()))
        self._session.commit()

        self._populate_fluid_names("./utils/fluid_names.txt")

        # Add a list of Fluids to the database
        print("Successfully intialized database")


    @contextmanager
    def session_context(self):
        '''context function that can be used to ensure the reuired overhead is always followed when querying the db
        
        Inteded use:
            function(*args, **kwargs):
                with session_context() as session:
                    val = session.query(class).filter(params).first()
        
        this will automatically rollback on error
        '''

        if not self._session:
            self._create_session()

        try:
            yield self._session
        
        except Exception as e:
            # on error, dont allow the db to be updated
            self._session.rollback()
            raise e
        finally:
            self._session.commit()


    def close_session(self):
        '''Util function to remove the current session'''
        if self._session:
            self._session.remove()
            self._session = None


    def _create_session(self):
        '''Private helper function to create a scoped session'''
        self._engine = create_engine(self._database_url)        
        self._SessionFactory = sessionmaker(self._engine) # create a persistent session
        self._session = scoped_session(self._SessionFactory)


    def _populate_fluid_names(self, filepath):
        '''private util method to populate the database with fluid names'''
        with open(filepath, "r") as fluid_names:
            for name in fluid_names:
                if name.strip():
                    self._session.add(Fluid(name=name.strip()))

        self._session.commit()
