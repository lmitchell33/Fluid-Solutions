from contextlib import contextmanager
from threading import Lock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

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
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None: 
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
        
        self._engine = create_engine(database_url)
        self._session = scoped_session(sessionmaker(self._engine))
        self._initialized  = True


    def initdb(self, Base):
        '''initalizes the database by dropping all tables then re-creating the 
        the tables.

        Args:
            Base {sqlalchemy.ext.declarative.base} -- base class that holds all tables
        '''

        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        print("Successfully intialized database")


    @contextmanager
    def session_context(self):
        '''context function that can be used to ensure the reuired overhead is always followed when querying the db
        
        Inteded use:
            function(*args, **kwargs):
                with session_context() as session:
                    val = session.query(class).filter(params).first()
                    # logic here
        
        this automatically creates and closes the session, as well as commits any changes and rolls back on errors
        '''
        session = self._session()

        try:
            yield session
            session.commit()
        
        except Exception as e:
            # on error, dont allow the db to be updated
            session.rollback()
            raise e

        finally:
            # cleanup garbage
            self._session.remove()
