import socket
from threading import Thread, Lock

from PyQt6.QtCore import pyqtSignal, QObject

class VitalsManager(QObject):
    '''
    Represents the method in which the the app will receive and process data,
    send it to the frontend for visualization and backend for ML inference.

    The data this class receives and processes may not be real, however it will
    mimic IEEE 11073 Protocol (Medical Device Communication) as it is the 
    international standard for all medical device communication.
    
    This protocol utilizes the Agent-Manager Model where multiple smaller agents,
    in this case the medical device(s), communication with a centralized manager.
    In this model, the agent sends status updates to the manager. This communication
    can be either "manager initiated" (the manager actively contacts the agent) 
    or "agent initiated" (the agent proactively reaches out to the manager).
    This class represents the 'manager' which will collect data from agent(s) who
    send information pertaining to vitals.
    '''
    vitals_data = pyqtSignal(dict)

    _instance = None
    _lock = Lock()

    def __new__(cls):
        '''Ensure only one instance of class is created, following the Singleton pattern'''
        if not cls._instance:
            with cls._lock:
                cls._instance = super(VitalsManager, cls).__new__(cls)
                cls._instance._initalized = False
        
        return cls._instance


    def __init__(self, host="0.0.0.0", port=8080):
        if self._initalized:
            return
        
        self._initalized = True
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = None
        self._running = False


    def start_server(self):
        '''Starts the server to listen for medical devices'''
        # Start the server and listen for medical devices on the socket (stream)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        
        self._running = True

        # run the server in a separate daemon so it does not block the mian thread
        socket_thread = Thread(target=self._listen, daemon=True)
        socket_thread.start()


    def _listen(self):
        '''Listen for incoming clients'''
        while self._running:
            conn, addr = self.server_socket.accept()

            try:
                self._handle_clients(conn)
            
            # Handle all errors gracefully
            except ConnectionError:
                print("Connection error with client")
            except Exception as e:
                print(f"Error while handling client connectionL: {e}")

            finally:
                print("Connection closed")

    
    def _handle_clients(self, connection):
        '''Hanldes a client connection'''
        while self._running:
            # receive data from the medical device
            data = connection.recv(1024).decode()
            if not data:
                break

            # parse/preprocess the data and emit it to the frontend
            # TODO: Implement the emitting part in the frontend
            
            print(data)
            # if data:
            #     self.vitals_data.emit(data)


    def stop_server(self):
        '''Stops the server'''
        # Stop everything
        self._running = False
        if self.server_socket:
            self.server_socket.close()

