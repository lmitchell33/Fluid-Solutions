import pytest
from pathlib import Path
from unittest.mock import MagicMock
from datetime import datetime

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


def test_inital_states(app):
    '''Ensures each of the textboxes start with value of empty string when page loads'''
    assert app.mrn_value.text() == ""
    assert app.lastname_value.text() == ""
    assert app.firstname_value.text() == ""
    assert app.weight_value.text() == ""
    assert app.height_value.text() == ""
    
    # Combo box has a different method
    assert app.gender_dropdown.currentText() == ""


def test_search_patient_success(qtbot, app, monkeypatch):
    """Test searching for a patient successfully."""
    mock_patient = MagicMock()
    mock_patient.patient_mrn = "12345"
    mock_patient.firstname = "John"
    mock_patient.lastname = "Doe"
    mock_patient.gender = 'male'
    mock_patient.dob = datetime.now().date()

    mock_coordinator = MagicMock()
    mock_coordinator.get_or_create_patient.return_value = mock_patient

    # Patch the coordinator inside the PatientWindow instance
    app._coordinator = mock_coordinator

    # Simulate entering an MRN
    app.mrn_value.setText("12345")

    # Simulate clicking the search button
    with qtbot.waitSignal(app.search_patient.clicked, timeout=500):
        app.search_patient.click()

    # Check that the UI updates correctly
    assert app.firstname_value.text() == "John"
    assert app.lastname_value.text() == "Doe"


def test_search_patient_failure(qtbot, app, monkeypatch):
    """Test searching for a non-existent patient."""
    mock_coordinator = MagicMock()
    mock_coordinator.get_or_create_patient.return_value = None  # Simulate no patient found

    app._coordinator = mock_coordinator
    app.mrn_value.setText("99999")

    with qtbot.waitSignal(app.search_patient.clicked, timeout=500):
        app.search_patient.click()

    # Since no patient was found, these fields should still be empty
    assert app.firstname_value.text() == ""
    assert app.lastname_value.text() == ""


@pytest.mark.parametrize("mrn_input", ["", "   "])
def test_search_patient_invalid_input(qtbot, app, mrn_input):
    """Test searching with an empty or invalid MRN."""
    app.mrn_value.setText(mrn_input)

    with qtbot.waitSignal(app.search_patient.clicked, timeout=500):
        app.search_patient.click()

    assert app.firstname_value.text() == ""
    assert app.lastname_value.text() == ""