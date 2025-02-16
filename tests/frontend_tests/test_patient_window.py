import pytest
import os
from unittest.mock import patch
from pathlib import Path

from app.database_manager import DatabaseManager
from app.frontend.patient_window import PatientWindow

@pytest.fixture(scope="module")
def mock_db():
    os.environ['DATABASE_URL'] = "sqlite:///:memory:"
    mock_databsae = DatabaseManager()
    mock_databsae.initdb()

    with patch("backend.managers.patient_manager.DatabaseManager") as patched_db:
        patched_db = mock_databsae

        yield patched_db

        mock_databsae.close_session()


@pytest.fixture
def app(qtbot, mock_db):
    '''fixture to create and setup an app to run the tests through'''
    ui_file_path = str(Path(__file__).parent.parent.parent.joinpath("app/frontend/views/patientWindow.ui"))

    test_app = PatientWindow(ui_file_path)
    qtbot.addWidget(test_app)
    return test_app


def test_components_exist(app):
    '''Ensure key UI components exist'''
    assert app.search_patient is not None
    assert app.mrn_value is not None
    assert app.lastname_value is not None
    assert app.firstname_value is not None
    assert app.gender_dropdown is not None
    assert app.dob_value is not None
    assert app.weight_value is not None
    assert app.height_value is not None