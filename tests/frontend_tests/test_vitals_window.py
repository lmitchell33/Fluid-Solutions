import pytest
from pathlib import Path
from unittest.mock import MagicMock
from datetime import datetime

from PyQt6.QtCore import QDateTime

from app.frontend.vitals_window import VitalsWindow

@pytest.fixture
def app(qtbot, patch_patient_manager, patch_fluid_manager):
    '''Fixture to create and set up the VitalsWindow for testing'''
    ui_file_path = Path(__file__).resolve().parents[2] / "app/frontend/views/vitalsWindow.ui"
    assert ui_file_path.exists(), f"UI file not found {ui_file_path}"
    test_app = VitalsWindow(ui_file_path)
    qtbot.addWidget(test_app)
    return test_app


def test_components_exist(app):
    '''Ensure key UI components exist'''
    assert app.popup_button is not None
    assert app.heart_rate_units is not None
    assert app.spo2_units is not None
    assert app.blood_pressure_units is not None
    assert app.map_units is not None
    assert app.rr_units is not None
    assert app.ppv_units is not None
    assert app.fluid_volume_units is not None
    assert app.current_datetime is not None


def test_datetime_setup(app):
    '''Ensure datetime is initialized properly'''
    assert app.current_datetime.displayFormat() == "hh:mm:ss a MMM dd, yyyy"
    assert isinstance(app.current_datetime.dateTime(), QDateTime)
    assert app.current_datetime.isReadOnly()


# def test_open_popup(app):
#     '''Test popup opens correctly and avoids duplicates'''
#     assert app.popup is None or not app.popup.isVisible()

#     app._open_popup()
#     assert app.popup is not None
#     assert app.popup.isVisible()

#     # Call again to ensure duplicate popup isn't created
#     existing_popup = app.popup
#     app._open_popup()
#     assert app.popup == existing_popup


def test_handle_popup_submission_success(app, monkeypatch):
    '''Test fluid submission success logic'''
    mock_patient = MagicMock(firstname="Jane", lastname="Doe", patient_mrn="123", gender="female", dob=datetime.now(), height=170, weight=65)
    app.patient_state.current_patient = mock_patient

    mock_manager = MagicMock()
    mock_manager.add_record.return_value = True
    monkeypatch.setattr(app, "_fluid_manager", mock_manager)

    app._handle_popup_submission("Saline", 500)
    mock_manager.add_record.assert_called_once()


def test_handle_popup_submission_failure(app, monkeypatch):
    '''Test fluid submission failure logic'''
    mock_patient = MagicMock(firstname="Jane", lastname="Doe", patient_mrn="123", gender="female", dob=datetime.now(), height=170, weight=65)
    app.patient_state.current_patient = mock_patient

    mock_manager = MagicMock()
    mock_manager.add_record.return_value = False
    monkeypatch.setattr(app, "_fluid_manager", mock_manager)

    app._handle_popup_submission("Saline", 500)
    mock_manager.add_record.assert_called_once()


def test_update_ui(app):
    '''Test _update_ui sets patient fields'''
    mock_patient = MagicMock(firstname="Jane", lastname="Doe", patient_mrn="123", gender="female", dob=datetime.now(), height=170, weight=65)
    app.patient_state.current_patient = mock_patient
    app._fluid_manager.get_total_fluid_volume = MagicMock(return_value=1000)

    app._update_ui()

    assert app.name_value.text() == "Jane Doe"
    assert app.mrn_value.text() == "123"
    assert app.total_fluid_value.text() == "1000"


def test_update_vitals(app):
    '''Test that vitals update the proper fields'''
    vitals_data = {
        "heartRate": 80,
        "meanArterialPressure": 70,
        "respiratoryRate": 10,
        "systolicBP": 120,
        "diastolicBP": 80,
        "spo2": 98
    }

    app._update_vitals(vitals_data)

    assert app.heart_rate_value.text() == "80"
    assert app.map_value.text() == "70"
    assert app.rr_value.text() == "10"
    assert app.spo2_value.text() == "98"
    assert app.blood_pressure_value.text() == "120 / 80"
    assert app.ppv_value.text() != ""  # Should be computed


@pytest.mark.parametrize("inputs, expected", [
    ((None, 80), ""),          # missing systolic
    ((120, None), ""),         # missing diastolic
    ((None, None), ""),        # missing both
    ((120, 80), "0.0"),        # first reading, sets min and max
    ((130, 70), "40.0"),       # next reading, variation = 40
])
def test_calculate_ppv(app, inputs, expected):
    systolic, diastolic = inputs
    result = app._calculate_ppv(systolic, diastolic)

    # bc this function keeps track of the min and max we need to prime it with inital data
    if (systolic, diastolic) == (130, 70):
        app._calculate_ppv(120, 80)  # prime it first
        result = app._calculate_ppv(130, 70)

    assert result == expected
