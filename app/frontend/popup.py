import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import pyqtSignal
from PyQt6 import uic

from backend.managers.fluid_manager import FluidManager

class PopupForm(QWidget):
    form_submitted = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        uic.loadUi("./frontend/views/popup.ui", self)

        self.fluid_manager = FluidManager()
        self._populate_fluids_dropdown()

        self.submit_button.clicked.connect(self.submit_form)


    def _populate_fluids_dropdown(self):
        '''Automatically populate the list of fluid names with those stored in the db'''
        fluids_dropdown = self.fluids_dropdown
        fluid_names = self.fluid_manager.get_all_fluid_names()
        fluids_dropdown.addItems(fluid_names)


    def submit_form(self):
        '''Emits the current data in the popup back to the vitals window and closes the popup'''
        selected_fluid = self.fluids_dropdown.currentText()
        volume_given = self.volume_given.text()
        self.form_submitted.emit(selected_fluid, volume_given)
        self.close()

    
    def close_event(self, event):
        '''Event to close the popup and set the visibility to False'''
        self.deleteLater()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PopupForm()
    window.show()
    sys.exit(app.exec())