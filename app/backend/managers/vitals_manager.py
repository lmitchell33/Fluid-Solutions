import socket
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor

from PyQt6.QtCore import pyqtSignal, QObject
from pyasn1.codec.ber.decoder import decode

from vitals_data_models import VitalSigns

class VitalsManager(QObject):
    '''
    Represents the method in which the the app will receive and process data,
    send it to the frontend for visualization and backend for ML inference.

    The data this class receives and processes may not be real, however it will
    mimic IEEE 11073 Protocol (Medical Device Communication) as it is the 
    international standard for all medical device communication. This class 
    very loosly follows this standard, implementing asn.1 modeled communication.
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


    def __init__(self, host="0.0.0.0", port=8080, max_workers=5):
        if self._initalized:
            return
        
        self._initalized = True
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = None
        self._running = False

        # allow up to 5 threads/connecitons simultaneously
        self.executor = ThreadPoolExecutor(max_workers=max_workers)


    def start_server(self):
        '''Starts the server to listen for medical devices'''
        # Start the server and listen for medical devices on the socket (stream)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # this allows quick rebinding
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        
        self._running = True

        # run the server in a separate daemon so it does not block the mian thread
        socket_thread = Thread(target=self._listen, daemon=True)
        socket_thread.start()


    def _listen(self):
        '''Listen for incoming clients'''
        while self._running:
            try:
                self.server_socket.settimeout(2) # avoid blocking
                conn, addr = self.server_socket.accept()
                self._handle_clients(conn)
            
            # Handle all errors gracefully
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Error while handling client connection: {e}")

    
    def _handle_clients(self, connection):
        '''Hanldes a client connection'''
        connection.settimeout(5) # prevent hanging connections
        
        try:
            while self._running:
                # receive data from the medical device
                data = connection.recv(1024)
                if not data:
                    break

                # convert the data to a dict, ensure it exists, then emit to the frontend
                output_data = self._process_data(data)
                if output_data:
                    self.vitals_data.emit(output_data)
        except (socket.timeout, ConnectionError):
            print("Connection error")
        finally:
            print("Closing connection")
            connection.close()


    def _process_data(self, encoded_data):
        '''Processes incoming pyasn1 data and converts it to a dict for further processing
        
        Args:
            encoded_data {bytes} -- pyasn1 encoded data
            
        Return:
            data {dict} -- the data decoded and wrapped into a dict
        '''
        try:
            decoded_data, _ = decode(encoded_data, VitalSigns())
            data = {} 

            # loop throuhg the data sent (pyasn1 bytes) and place it into a dict for further processing
            for field in decoded_data:
                data[field] = str(decoded_data[field]['value'])

            return data
        except Exception as e:
            return None


    def stop_server(self):
        '''Stops the server'''
        # Stop everything
        if self._running:
            self._running = False
            print("Stopping the socket server for the vitals manager")

            try:
                # stops the socket from sending and receing data immediately
                self.server_socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                # socket is already closed
                pass

            # closes the socket
            self.server_socket.close()
            self.executor.shutdown(wait=False)
            print("Stopped vitals manager")
