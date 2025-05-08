import sys
import argparse

from PyQt6.QtCore import QFile, QTextStream
from PyQt6.QtWidgets import QApplication
from apscheduler.schedulers.qt import QtScheduler
from apscheduler.triggers.cron import CronTrigger

from database_manager import DatabaseManager
from backend.managers.api_manager import EpicAPIManager
from backend.managers.fluid_manager import FluidManager
from backend.managers.ml_manager import MLManager
from backend.managers.patient_manager import PatientManager
from backend.managers.vitals_manager import VitalsManager
from backend.coordinator import Coordinator

from frontend.router import Router
from frontend.patient_window import PatientWindow
from frontend.vitals_window import VitalsWindow


def load_stylesheet(stylesheet):
    '''util function to load in a QSS stylesheet to apply to the app as a whole
    This will apply to ALL windows in the app unless a stylesheet is applied directly to the other window
    
    Args:
        stylesheet {str} -- path to the .qss file containing the styling
    
    Returns:
        stream {QTextStream} -- PyQt obj containing the styling information needed to pass into QApplication.setStyleSheet()
    '''
    file = QFile(stylesheet)
    
    if not file.open(QFile.OpenModeFlag.ReadOnly):
        raise FileNotFoundError("Stylesheet not found, try running from the Fluid-Solutions/app directory")

    # read the stylesheet and save the qss contents for styling
    stream = QTextStream(file)
    qss_content = stream.readAll()
    file.close()
    return qss_content


def build_dependencies():
    '''Builds dependencies for the app, a scuffed version of a factory pattern to allow for dependency injection'''
    db_manager = DatabaseManager()
    vitals_manager = VitalsManager()
    api_manager = EpicAPIManager()
    ml_manager = MLManager(model_type='xgb', binary=False, max_cache_size=100)
    
    fluid_manager = FluidManager(db_manager)
    patient_manager = PatientManager(db_manager)
    
    coordinator = Coordinator(fluid_manager, api_manager, patient_manager)

    return {
        "db_manager": db_manager,
        "vitals_manager": vitals_manager,
        "ml_manager": ml_manager,
        "api_manager": api_manager,
        "fluid_manager": fluid_manager,
        "patient_manager": patient_manager,
        "coordinator": coordinator
    }


def configure_scheduler(coordinator:Coordinator):
    '''Create and configure a cron scheduler that works within Qt's event loop'''
    scheduler = QtScheduler()
    scheduler.add_job(coordinator.remove_inactive_patients, CronTrigger(hour=0, minute=0))
    return scheduler


def run(args):
    '''Initalizes the router and start the PyQT application'''
    dependencies = build_dependencies()

    try:
        # initalizes the database if the --initdb flag is passed
        if args.initdb:
            db = DatabaseManager()
            db.initdb()
            return

        app = QApplication(sys.argv)
        app.setStyleSheet(load_stylesheet(stylesheet="frontend/stylesheets/window.qss"))

        # on app startup, remove all inactive patients, and create a cron scheduler
        # to remove inactive patients every night at midnight, if the app is left on
        dependencies['coordinator'].remove_inactive_patients()
        scheduler = configure_scheduler(dependencies['coordinator'])
        scheduler.start()

        # initalize the windows and specify the routing for each window
        patient_window = PatientWindow(
            ui_file="frontend/views/patientWindow.ui",
            coordinator=dependencies['coordinator'],
            patient_manager=dependencies['patient_manager'],
        )

        vitals_window = VitalsWindow(
            ui_file="frontend/views/vitalsWindow.ui",
            fluid_manager=dependencies['fluid_manager'],
            vitals_manager=dependencies['vitals_manager'],
            ml_manager=dependencies['ml_manager'],
        )

        patient_window.routes_to = vitals_window
        vitals_window.routes_to = patient_window

        # router uses a stackedwidget
        router = Router(patient_window, vitals_window)
        screen = app.primaryScreen()
        geometry = screen.geometry()
        router.resize(int(geometry.width()/(3)), int(geometry.height()/(2)))

        # start the socket server for the vitals manager.
        # NOTE: if this was IRL then I would probably start this differently, but
        # this is a demo and I don't have time to figure soemething else out
        dependencies['vitals_manager'].start_server()

        # start the app and router, by default the patient window is shown
        router.show() 
        app.exec()

    finally:
        # cleanup
        dependencies['db_manager'].close_session()
        dependencies['vitals_manager'].stop_server()


def parse_arguments(args=None):
    '''Parses input arguments from stdin, creates a flag for initalizing the database
    intended use from the cli: "python3 app.py -initdb"

    Kwargs:
        args {argparse obj} -- list of args to parse, default is cli args (sys.argv)
    
    Returns:
        parsed_args {argparse obj} -- argparse obj with the arguments from the cli
    '''
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--initdb", action="store_true", default=False, help="Initalize the database")

    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_arguments()
    run(args)