from pathlib import Path
from collections import deque, Counter

import xgboost as xgb
import joblib
import numpy as np

from PyQt6.QtCore import pyqtSignal, QObject

class MLManager(QObject):
    '''ML Manager class whose job is to load in a specified model, and perform
    inference.
    
    Attributes:
        model: The loaded machine learning model
    '''
    prediction_ready = pyqtSignal(dict)

    def __init__(self, model_type='xgb', binary=False, max_cache_size=100):
        '''Initalize the MLManager instance (runs only once)
        
        Args:
            model_type {str} -- The type of model to load. Currently supports 'xgb' and 'rf'. Default is 'xgb'.
            binary {bool} -- Whether binary or ternary classificaiton model should be loaded. Default is Ternary.
            max_cache_size {int} -- The maximum size of the cache for batched inference.
        '''        
        super().__init__()
        self.model = None
        self._model_type = model_type.lower()
        self._binary_predictor = binary

        # cahce for batched inference
        self._data_cache = deque(maxlen=max_cache_size)

        # filepath for the dir holding all models should be ~/Fluid-Solutions/app/models
        self._model_dir = Path(__file__).parent.parent.parent.joinpath("models")
        if not self._model_dir.exists():
            print(f"Directory containing the model file not found {self._model_dir}")


    def load_model(self):
        '''Load the specified model if not already loaded'''
        if self.model:
            return
        
        try:
            self.model = self._load_model()
        except Exception as e:
            raise RuntimeError(f"Failed to load {self._model_type} model: {e}")


    def _load_model(self):
        '''Util method to load the appropriate model.'''        
        if self._model_type == "xgb":
            # model_file = "xgboost_model.json" if not self._binary_predictor else "xgboost_binary_model.json"
            model_file = "unsupervised_data_xgboost.json" if not self._binary_predictor else "xgboost_binary_model.json"
            model_path = self._model_dir / model_file

            if not model_path.exists():
                raise FileNotFoundError(f"Model file not found: {model_path}")

            model = xgb.XGBClassifier()
            model.load_model(str(model_path))
            return model

        elif self._model_type == "rf":
            # load in the rf model from the saved model
            model_file = "random_forest_model.pkl" if not self._binary_predictor else "random_forest_binary_model.pkl"
            model_path = self._model_dir / model_file

            if not model_path.exists():
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            return joblib.load(f'{self._model_dir}/{model_file}.pkl')

        else:
            raise FileNotFoundError(f"{self._model_type} file not found")


    def add_to_cache(self, data):
        '''Add the datapoint to the cache for batched inference'''
        self._data_cache.append(data)


    def run_batched_inference(self):
        '''Run batched inference on the cached data'''
        if self.model is None:
            self.load_model()

        if len(self._data_cache) == 0:
            return

        # batched inference using majority voting to determine the final prediction
        predictions = []
        print(f"The length of the cache is: {len(self._data_cache)}")
        for vitals_data in self._data_cache:
            curr_prediction = self._raw_predict(vitals_data)
            predictions.append(curr_prediction)

        if predictions:
            # use a majority vote to determine the final prediction
            most_common_pred = Counter(predictions).most_common(1)[0][0]
            self.prediction_ready.emit(self._post_process(most_common_pred))


    def predict(self, data):
        '''Perform inference using the loaded model
        
        Args: 
            data: Input data for prediction in the format expected by the model

        Returns:
            Model Prediction {dict} -- label:suggested action 
            where label = low, high, normal (or normal vs. not normal) 
            and suggested action = administer fluid etc...
        '''
        if self.model is None:
            self.load_model()

        try: 
            prediction = self._raw_predict(data)
            return self._post_process(prediction)
        except Exception as e:
            print(f"Failed to make prediction {e}")


    def _raw_predict(self, data):
        '''Perform inference using the loaded model without post-processing'''
        if self.model is None:
            self.load_model()

        preprocess_data = self._preprocess(data)
        return self.model.predict(preprocess_data)[0]

    
    def _post_process(self, prediction):
        '''Post-process a prediction made by the model'''
        if self._binary_predictor:
            prediction_mapping  = {
                0 : {'label' : 'abnormal blood volume', 'suggested_action':'evaluate and consider action'},
                1 : {'label' : 'euvolemic', 'suggested_action':'maintain current status'},
            }
        else:
            prediction_mapping  = {
                0 : {'label' : 'hypervolemia', 'suggested_action':'consider fluid removal'},
                1 : {'label' : 'hypovolemia', 'suggested_action':'consider fluid administration'},
                2 : {'label' : 'euvolemia', 'suggested_action':'maintain current status'}
            }

        return prediction_mapping.get(prediction, {"label": "N/A", "suggested_action": "N/A"})


    def _preprocess(self, data):
        '''Preprocess the inference data to match the model's expected input format.
    
        The function ensures data is structured correctly for inference.
        It currently handles list inputs and will be extended to support dictionaries.
        
        expected array shape for the batched inference is:
        [[14. 91. 90. 63. 81. 96.  0. 18.]]

        Args:
            data (list or dict): Input data to preprocess.
        '''
        feature_map = {
            0: 'respiratoryRate',
            1: 'heartRate',
            2: 'meanArterialPressure',
            3: 'diastolicBP',
            4: 'systolicBP',
            5: 'spo2',
            6: 'age',
            7: 'pulsePressure'
        }

        if isinstance(data, dict):
            features = []
            for idx, feature_name in feature_map.items():
                # manually put the features into their correct positions
                features.insert(idx, float(data.get(feature_name, 0)))

            # reshape the array to match the model's expected input
            array = np.array(features).reshape(1, -1)
            return array

        # must convert data to numpy array and check its dimensions to match
        # what we trained the model with
        elif isinstance(data, list):
            # just assuming the data is in the correct order
            array = np.array(data, dtype=float)
            if array.ndim == 1:
                array = array.reshape(1, -1)

            if array.shape[1] != len(feature_map):
                print("inputted list has incorrect size")

            return array

        else:
            raise TypeError("Inputted data for preprocessing must be list or dict")


if __name__ == "__main__":
    model_type = "xgb"
    model = MLManager(model_type=model_type)
    model.load_model()

    output_mapping = {
        0 : "high",
        1 : "low",
        2 : "normal"
    }

    # example row from the data
    data_low = [17.0, 73.0, 83.0, 55.0, 131.0, 98.0, 45, 76.0]
    # example_test_low = [i+2 for i in data_low]
    extreme_test_low = [13.0, 60.0, 60, 50, 100, 97.0, 45, 50]

    data_high = [13.0, 60.0, 103.0, 75.0, 148.0, 97.0, 45, 73.0]
    # example_test_high = [i+2 for i in data_high]
    extreme_test_high = [13.0, 60.0, 105, 75, 165, 97.0, 45, 90]

    data_noraml = [21.0, 108.0, 76.3, 63.7, 117.4, 94.0, 45, 53.8]
    # example_test_normal = [i+2 for i in data_noraml]

    prediction = model.predict(extreme_test_low)
    
    if model_type == "xgb":
        print(prediction)
    elif model_type == "rf":
        print(prediction)
