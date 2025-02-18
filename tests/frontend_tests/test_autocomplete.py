import pytest
from pathlib import Path

from app.frontend.utils.autocomplete import AutoComplete

@pytest.fixture
def patient_mock_list():
    pass 


@pytest.fixture
def options_mock_data():
    pass


@pytest.fixture
def autocomplete_widget(qtbot, patient_mock_list, options_mock_data):
    autocomplete = AutoComplete(patient_mock_list, options_mock_data)
    qtbot.addWidget(autocomplete)
    return autocomplete