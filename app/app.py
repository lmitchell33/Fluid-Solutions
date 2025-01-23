import sys
import argparse

from PyQt6.QtCore import QFile, QTextStream
from PyQt6.QtWidgets import QApplication

from frontend.router import Router
from frontend.patient_window import PatientWindow
from frontend.vitals_window import VitalsWindow
from database_models import Base

from database_manager import DatabaseManager


def load_stylesheet(stylesheet):
    '''util function to load in a QSS stylesheet to apply to the app as a whole
    NOTE: This will apply to ALL windows in the app unless a stylesheet is applied directly to the other window
    Args:
        stylesheet {str} -- path to the .qss file containing the styling
    
    Returns:
        stream {QTextStream} -- PyQt obj containing the styling information needed to pass into QApplication.setStyleSheet()
    '''
    file = QFile(stylesheet)
    
    if not file.open(QFile.OpenModeFlag.ReadOnly):
        raise FileNotFoundError("Stylesheet not found, try running from the Fluid-Solutions/app directory")

    # read the stylesheet and save the qss contents then close the file to save memory
    stream = QTextStream(file)
    qss_content = stream.readAll()
    file.close()
    return qss_content


def main():
    '''Initalizes the router and start the PyQT application'''
    # starts the application from the cli and initalizes the router
    app = QApplication(sys.argv)

    # get the current size of the screen so we can resize the new window when it displays
    screen = app.primaryScreen()
    geometry = screen.geometry()

    # initalize the windows and specify which each window routes to
    patient_window = PatientWindow()
    vitals_window = VitalsWindow()
    patient_window.routes_to = vitals_window
    vitals_window.routes_to = patient_window

    # router facilitates the routing using a stackedwidget
    router = Router(patient_window, vitals_window)

    # resize the window to 1.5x that of the current screen
    router.resize(int(geometry.width()/(1.5)), int(geometry.height()/(1.5)))

    # set the stylesheet and display the screen
    app.setStyleSheet(load_stylesheet("frontend/stylesheets/window.qss"))
    router.show() # by default, this shows the patient window

    sys.exit(app.exec())


def parse_arguments(args=None):
    '''Parses input arguments from stdin, creates a flag for initalizing the database
    intended use from the cli: "python3 app.py -initdb"

    Kwargs:
        args {argparse obj} -- list of args to parse, default is cli args (sys.argv)
    
    Returns:
        parsed_args {argparse obj} -- argparse obj with the arguments from the cli
    '''
    
    # intended use: "python3 app.py --initdb" to initalize the database
    parser = argparse.ArgumentParser()
    parser.add_argument("--initdb", action="store_true", default=False, help="Initalize the database")

    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_arguments()

    db = DatabaseManager()

    if args.initdb:
        db.initdb(Base)
    else:    
        main()