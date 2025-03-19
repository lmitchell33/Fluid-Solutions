from threading import Lock

class MLManager:
    '''ML Manager class whose job is to load in a specified model, and perform
    inference using said model. This is singleton, beucase I do not want multiple
    instances performing infernece bc the inference is run locally and could 
    take up significant resources
    
    Methods:
        
    '''

    _instance = None
    _lock = Lock()

    def __new__(cls, model='xgb'):
        '''Ensure only one instance of class is created, following the Singleton pattern'''
        if not cls._instance:
            with cls._lock:
                cls._instance = super(MLManager, cls).__new__(cls)
                cls._instance._initalized = False
                cls._instance.model = model # store the model in the instance
        
        return cls._instance
    
    def __init__(self, model='xgb'):
        
        if self._initalized:
            return
        
        self._initalized = True
        self.model = model # set the model on the first initalization


if __name__ == "__main__":
    pass
    # test to ensure singleton:
    # ml1 = MLManager(model="rf")
    # print(ml1.model)

    # ml2 = MLManager(model="xgb")
    # print(ml1.model)
