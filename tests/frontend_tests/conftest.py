import pytest
from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt


@pytest.fixture(scope="session", autouse=True)
def no_gui():
    """Prevents GUI pop-ups during testing."""
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs)


@pytest.fixture(autouse=True)
def mock_message_box(monkeypatch):
    """Mock the QMessageBox to prevent pop-ups during tests."""
    monkeypatch.setattr(QMessageBox, "information", MagicMock())
    monkeypatch.setattr(QMessageBox, "warning", MagicMock())


@pytest.fixture(scope="module")
def patch_patient_manager(mock_db):
    '''Patches the DatabaseManager declaration in the PatientManager class'''
    # NOTE: This is only becuase the DatabaseManager is the result of a tree of imports into the patient window
    with patch("backend.managers.patient_manager.DatabaseManager", return_value=mock_db):
        yield mock_db


@pytest.fixture(scope="module")
def patch_fluid_manager(mock_db):
    '''Patches the DatabaseManager declaration in the FluidManager class'''
    with patch("backend.managers.fluid_manager.DatabaseManager", return_value=mock_db):
        yield mock_db