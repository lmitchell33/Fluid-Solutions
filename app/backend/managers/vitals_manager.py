import socket

class VitalsManager:
    '''
    Represents the method in which the the app will receive and process data,
    send it to the frontend for visualization and backend for ML inference.
    Due to the ambiguous nature of the method in which we recieve the data,
    the class will mostly be a wrapper. 

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

    def __init__(self): 
        pass

