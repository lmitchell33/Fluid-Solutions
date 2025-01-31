from PyQt6.QtWidgets import QStackedWidget

class Router(QStackedWidget):
    """
    A class to manage routing between multiple windows in the application.
    
    A stacked widget was chosen becuase it loads all views into memory 
    when initalized making the switching of the views more efficent because of 
    less load time. However, if the model inference or SQLAlchemy uses too much 
    RAM change this to a more simple routing method where you simply show and 
    hide the windows, that way the number of views loaded into memroy at once 
    is limited to 1.
    
    Inits and handles interactions between the inputed windows. This design is 
    flexible, allowing for as many windows as you want. 

    Methods:
        show_window(window): Switches the displayed window to the specified one
    """

    def __init__(self, *windows):
        '''Constructor for the Router, creates and adds all windows 
        to the QStackedWidget. Also sets up the button click connections to 
        handle the physical routing between the windows
        '''
        super().__init__()

        self._windows = windows

        try:
            # add each widget to the stacked widget
            for window in self._windows:
                self.addWidget(window)
        except Exception as e:
            print(f"Window not found: {e}")

        # set the inital (default) window to be the first window added to the router
        self.setCurrentWidget(self._windows[0])

        self._setup_routing()


    def _setup_routing(self):
        '''Dynamically connects routing buttons between all windows'''
        try:
            for window in self._windows: 
                # get the routing button for the current window 
                routing_button = window.get_routing_button()

                if routing_button:
                    button = routing_button
                    
                    if button:
                        # when the button is clicked, display the window it routes to
                        button.clicked.connect(lambda _, curr_window=window: self.show_window(curr_window.routes_to))
        
        except Exception as e:
            # catchall
            print(f"Error occured: {e}")
            raise e                    


    def show_window(self, window):
        ''' Sets the current window being shown to the specified window
        Args:
            window {QWidget or QMainWindow} -- The window to be displayed
            
        Returns:
            None
        ''' 
        self.setCurrentWidget(window)
        window.mrn_value.setFocus() #hackey fix so the datetime isnt highlighted when screens change