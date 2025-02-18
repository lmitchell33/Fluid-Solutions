import pytest
from pathlib import Path

from app.frontend.patient_window import PatientWindow


@pytest.fixture
def app(qtbot, patch_patient_manager):
    '''fixture to create and setup an app to run the tests through'''
    ui_file_path = Path(__file__).resolve().parents[2] / "app/frontend/views/patientWindow.ui"
    assert ui_file_path.exists(), f"UI file not found {ui_file_path}"
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