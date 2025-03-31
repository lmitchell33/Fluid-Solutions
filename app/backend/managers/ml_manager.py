from threading import Lock
from pathlib import Path
import xgboost as xgb
import joblib
import numpy as np

class MLManager():
    '''ML Manager class whose job is to load in a specified model, and perform
    inference using said model. This is singleton, beucase I do not want multiple
    instances performing infernece bc the inference is run locally and could 
    take up significant resources
    
    Methods:
        
    '''

    _instance = None
    _lock = Lock()

    def __new__(cls, model_type='xgb', binary=False):
        '''Ensure only one instance of class is created, following the Singleton pattern'''
        if not cls._instance:
            with cls._lock:
                cls._instance = super(MLManager, cls).__new__(cls)
                cls._instance._initalized = False
        
        return cls._instance
    

    def __init__(self, model_type='xgb', binary=False):
        '''Initalize the MLManager instance (runs only once)'''
        if self._initalized:
            return
        
        self._initalized = True
        self._model_type = model_type
        self._binary_predictor = binary
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
            model_file = "xgboost_model.json" if not self._binary_predictor else "xgboost_binary_model.json"

            # load an xgb classifier from the saved model
            model = xgb.XGBClassifier()
            model.load_model(f'{self._model_dir}/{model_file}')
            return model

        elif self._model_type == "rf":
            # load in the rf model from the saved model
            model_file = "random_forest_model.pkl" if not self._binary_predictor else "random_forest_binary_model.pkl"
            return joblib.load(f'{self._model_dir}/{model_file}.pkl')

        else:
            raise FileNotFoundError(f"{self._model_type} file not found")


    def predict(self, data):
        '''Perform inference using the loaded model
        
        Args: 
            data: Input data for prediction in the format expected by the model

        Returns:
            Model Prediction {dict} -- key:val => label:suggested action 
            where label = low, high, normal (or normal vs. not normal) 
            and suggested action = administer fluid etc...
        '''
        if self.model is None:
            self.load_model()

        data = self._preprocess(data)

        return self.model.predict(data)

    
    def _post_process_predict(self, data):
        '''Post-process a prediction made by the model'''
        if self._binary_predictor:
            PREDICTION_MAPPING = {
                0 : {'label' : 'not normal', 'suggested_action':'administer or remove fluids'},
                1 : {'label' : 'normal', 'suggested_action':'nothing'},
            }
        else:
            PREDICTION_MAPPING = {
                0 : {'label' : 'high', 'suggested_action':'remove fluids'},
                1 : {'label' : 'low', 'suggested_action':'administer fluids'},
                2 : {'label' : 'normal', 'suggested_action':'nothing'}
            }

        prediction = self.predict(data)[0]

        return PREDICTION_MAPPING.get(prediction, {"label": "N/A", "suggested_action": "N/A"})


    def _preprocess(self, data):
        '''Preprocess the inference data to match the model's expected input format.
    
        The function ensures data is structured correctly for inference.
        It currently handles list inputs and will be extended to support dictionaries.

        Expected feature order:
            0: 'respiratory_rate'
            1: 'heart_rate'
            2: 'mean_arterial_pressure'
            3: 'diastolic_arterial_pressure'
            4: 'systolic_arterial_pressure'
            5: 'spo2'
            6: 'pulse_pressure'
        
        Args:
            data (list or dict): Input data to preprocess.
            
        Returns:
            np.ndarray: Preprocessed input data.
        '''
        EXPECTED_FEATURE_ORDER = {
            0: 'respiratoryRate',
            1: 'heartRate',
            2: 'meanArterialPressure',
            3: 'diastolicBP',
            4: 'systolicBP',
            5: 'spo2',
            6: 'pulsePressure'
        }

        if isinstance(data, dict):
            arr = []
            for key, value in EXPECTED_FEATURE_ORDER.items():
                # iterate through the vitals and insert the features into their
                # correct positions
                arr.insert(key, float(data.get(value, 0)))
            array = np.array(arr)
            if array.ndim == 1:
                array = array.reshape(1, -1)
            return array

        if not isinstance(data, list):
            print("Cannot preporcess data, invalid input type")
            raise TypeError("List or dict expected")
        
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

    # high -> 0 -> when BVS is high, fluid must be taken away -> bp is low 
    # low -> 1 -> when BVS is low, fluid must be given -> bp is high
    # normal -> 2 -> when BVS normal, nothing happens - bp is normal

    output_mapping = {
        0 : "high",
        1 : "low",
        2 : "normal"
    }

    # It seems that the base random forest model is doing a horrible job of picking
    # up on the trends of this data, it typically classifies everything that is high
    # and everyhing that is low as low.

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
        print(prediction)
    elif model_type == "rf":
        print(prediction)