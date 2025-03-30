from threading import Lock
from pathlib import Path
import xgboost as xgb
import joblib
import numpy as np


from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import pandas as pd

class MLManager:
    '''ML Manager class whose job is to load in a specified model, and perform
    inference using said model. This is singleton, beucase I do not want multiple
    instances performing infernece bc the inference is run locally and could 
    take up significant resources
    
    Methods:
        
    '''

    _instance = None
    _lock = Lock()

    def __new__(cls, model_type='xgb'):
        '''Ensure only one instance of class is created, following the Singleton pattern'''
        if not cls._instance:
            with cls._lock:
                cls._instance = super(MLManager, cls).__new__(cls)
                cls._instance._initalized = False
        
        return cls._instance
    

    def __init__(self, model_type='xgb'):
        '''Initalize the MLManager instance (runs only once)'''
        if self._initalized:
            return
        
        self._initalized = True
        self._model_type = model_type
        self.model = None

        # get the filepath to the directory holding the model files
        self._model_dir = Path(__file__).parent.parent.parent.joinpath("models")


    def load_model(self):
        '''Load the specified model if not already loaded'''
        if self.model is not None:
            return
        
        try:
            self.model = self._load_model()
        except Exception as e:
            raise RuntimeError(f"Failed to load {self._model_type} model: {e}")
    

    def _load_model(self):
        '''Private helper function to load the appropriate model.'''        
        if self._model_type == "xgb":
            # load an xgb classifier from the saved model
            model = xgb.XGBClassifier()
            model.load_model(f'{self._model_dir}/xgboost_model.json')
            return model

        elif self._model_type == "rf":
            # load in the rf model from the saved model
            return joblib.load(f'{self._model_dir}/random_forest_model.pkl')

        else:
            raise FileNotFoundError(f"{self._model_type} file not found")


    def predict(self, data):
        '''Perform inference using the loaded model
        
        Args: 
            data: Input data for prediction in the format expected by the model

        Returns:
            Model Prediction {str} -- string 
        '''
        if self.model is None:
            self.load_model()

        data = self._preprocess(data)

        return self.model.predict(data)


    def _preprocess(self, data):
        '''Preprocess the inference data to ensure it matches what the data 
        was trained with
        '''
        if isinstance(data, dict):
            # TODO: handle this later
            pass

        # lets just assume we will get the data in the correct order and
        # as a list, for now
        arr = np.array(data)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        return arr



if __name__ == "__main__":
    # test see if this actually works:
    model_type = "xgb"
    model = MLManager(model_type=model_type)
    model.load_model()

    # what is importnat to rememeber here is that the heart is trying to keep the
    # blood at equilibrium, therefore, if the volume is high then the bp is low
    # and when the volume is low, the bp is high?

    # high -> 0 -> when BVS is high, fluid must be taken away -> bp is low 
    # low -> 1 -> when BVS is low, fluid must be given -> bp is high
    # normal -> 2 -> when BVS normal, nothing happens - bp is normal

    output_mapping = {
        0 : "high",
        1 : "low",
        2 : "normal"
    }

    #  'respiratory_rate' 
    #  'heart_rate'
    #  'mean_arterial_pressure'
    #  'diastolic_arterial_pressure'
    #  'systolic_arterial_pressure'
    #  'spo2'
    #  'pulse_pressure'

    # It seems that the base random forest model is doing a horrible job of picking
    # up on the trends of this data, it typically classifies everything that is high
    # and everyhing that is low as low.
    # the xgboost, however, is doing a much better job at picking up on the trends and
    # at least picking up on the extreme patterns

    # example row from the data
    data_low = [17.0, 73.0, 83.0, 55.0, 131.0, 98.0, 76.0]
    # example_test_low = [i+2 for i in data_low]
    extreme_test_low = [13.0, 60.0, 60, 50, 100, 97.0, 50]

    data_high = [13.0, 60.0, 103.0, 75.0, 148.0, 97.0, 73.0]
    # example_test_high = [i+2 for i in data_high]
    extreme_test_high = [13.0, 60.0, 105, 75, 165, 97.0, 90]

    data_noraml = [21.0, 108.0, 76.3, 63.7, 117.4, 94.0, 53.8]
    # example_test_normal = [i+2 for i in data_noraml]

    prediction = model.predict(extreme_test_low)[0]
    
    if model_type == "xgb":
        print(output_mapping[prediction])
    elif model_type == "rf":
        print(prediction)