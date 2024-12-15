from contextlib import contextmanager

from app import db_session

def session_wrapper(func):
    '''wrapper function for functions that will query the db used to ensure the session is was closed to prevent memory leaks
    
    Inteded use:
        @session_wrapper
        function(args, kwargs):
            do database stuff here

    this is automatically create and close the session, as well as commit any changes on success, and  perform a rollback if an error occurs. 
    '''
    def wrapper(*args, **kwargs):

        try:
            result = func(*args, **kwargs)
            db_session.commit()
            return result

        except Exception as e:
            db_session.rollback()
            raise e
    
        finally:
            db_session.close()
    
    return wrapper


@contextmanager
def session_context():
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