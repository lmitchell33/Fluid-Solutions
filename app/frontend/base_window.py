from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

class BaseWindow(QMainWindow):
    '''
    Base class for creating windows from .ui files. All shared methods between all windows should
    go into this class

    Methods:
        None (add to this comment if you add a method)
    '''

    def __init__(self, ui_file):
        ''' Constructor for the BaseWindow class, loads the specified .ui file
        Args:
            ui_file {str} -- Filepath to the .ui file to load. These files should all be in the /frontend/views/ directory
        
        Returns:
            None 
        '''
        super().__init__()
        uic.loadUi(ui_file, self)