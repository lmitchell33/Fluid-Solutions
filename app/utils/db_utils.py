from contextlib import contextmanager

@contextmanager
def session_context():
    from app import db_session 
    #NOTE: this import must be inside the context in order to prevent circular imports
    '''context function that can be used to ensure the reuired overhead is always followed when querying the db
    
    Inteded use:
        function(args, kwargs):
            with session_context() as session:
                val = session.query(class).filter(params).first()
                # logic here
    
    this automatically creates and closes the session, as well as commits any changes and rolls back on errors
    '''

    try:
        yield db_session
        db_session.commit()
    
    except Exception as e:
        db_session.rollback()
        raise e

    finally:
        db_session.close()