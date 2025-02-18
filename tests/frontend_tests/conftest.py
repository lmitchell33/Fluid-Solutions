import pytest
from unittest.mock import patch

@pytest.fixture(scope="module")
def patch_patient_manager(mock_db):
    '''Patches the DatabaseManager declaration in the PatientManager class'''
    # NOTE: This is only becuase the DatabaseManager is the result of a tree of imports into the patient window
    with patch("backend.managers.patient_manager.DatabaseManager", return_value=mock_db):
        yield mock_db