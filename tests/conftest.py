import sys
import os
import pytest

# add the app directory to the system path to allow the modules to be imported
APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../app"))

if APP_DIR not in sys.path:
    sys.path.append(APP_DIR)

@pytest.fixture(scope="module")
def mock_db():
    '''mocks an instance to the DatabaseManager class'''
    from app.database_manager import DatabaseManager
    DatabaseManager._instance = None
    os.environ['DATABASE_URL'] = "sqlite:///:memory:"
    mock_database = DatabaseManager()
    mock_database.initdb()

    yield mock_database

    mock_database.close_session()
