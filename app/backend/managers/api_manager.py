import os
import requests
import time
from xml.etree import ElementTree

from backend.epic.auth.auth import get_access_token, create_jwt

class EpicAPIManager:
    '''Class to manage the Epic API requests.
    
    Properties:
        access_token {str} -- access token for the Epic API session. Typically valid for 3600 seconsd.

    Methods:
        search_patient(**kwargs) - Search for patient ID and information from Epic
        get_patient_data(patient_id) -- get patient data from Epic 
        get_patient_vitals(observation_id) -- get patient vitals from Epic
        get_inactive_patients(patients) -- get a list of patients who are inactive
    '''    
    def __init__(self):
        '''Initialize the API Manager, ensuring initialization is done only once.'''

        # urls for each of the Epic API endpoints we are using
        self.search_patient_url = os.getenv("SEARCH_PATIENT_URL")
        self.vitals_url = os.getenv("READ_VITALS_URL")
        self.read_patient_url = os.getenv("READ_PATIENT_URL")

        # auth info for the session
        self._jwt = create_jwt()  
        self._access_token = None 
        self._access_token_expr = None 

        # specify the headers for each request
        self.headers = {
            "Authorization" : f"Bearer {self.access_token}",
            "Content-Type" : "application/json"
        }


    @property
    def access_token(self):
        '''
        Property of the class to get the access token and ensure its not expired.
        This always ensures that we have a valid access token before making any requests
        '''
        
        # check if the token is expired and get a new one if it is
        if (not self._access_token) or (time.time() >= self._access_token_expr):
            self._get_new_access_token() 
        
        return self._access_token


    def _get_new_access_token(self):
        '''Private method to get a new access token from Epic'''
        if not self._jwt:
            self._jwt = create_jwt()
        
        epic_auth_response = get_access_token(self._jwt)

        # set the token and the token's expiration time based on the response
        self._access_token = epic_auth_response.get("access_token", "")
        self._access_token_expr = time.time() + epic_auth_response.get("expires_in", "")


    def search_patient(self, **kwargs):
        '''Method to search Epic for a patient

        # NOTE: This function is currently only setup to except a singular patient
        as the result of the serach. If there are more than one then a popup has to be
        created that will allow the user to choose which patient it is.
        
        Kwargs:
            **kwargs {dict} -- search parameters for the patient. A list of valid parameters is shown below
                - _id
                - address
                - birthdate
                - family 
                - gender 
                - given 
                - identifier 

        Returns:
            patient_data {str} -- patient data from Epic        
        '''

        # Define the allowed search parameters for the API (from Epic)
        allowed_keys = [
            "_id", "address", "birthdate", "family", "gender", "given", "identifier",
        ]
    
        # filter for the kwargs so that only the valid serach parameters are used
        payload = {k: v for k, v in kwargs.items() if k in allowed_keys}

        if not payload:
            print("Invalid arugments, please ensure the parameters are valid")
            return None

        try:
            # request info from epic based on the parameters
            response = requests.get(self.search_patient_url, payload, headers=self.headers)
            response.raise_for_status()

            patient = {}

            # parse the xml response from epic
            xml = response.content
            tree = ElementTree.fromstring(xml)

            for element in tree.iter():
                patient[element.tag.removeprefix("{http://hl7.org/fhir}")] = element.get("value")

            if patient.get('total', '0') == '0':
                return None
        
            return patient

        except Exception as e:
            print(f"Error with seraching epic. Status code: {response.status_code}: ", e)
            return None


    def get_patient(self, patient_id):
        '''Method to get patient data from Epic
        
        Args:
            patient_id {str} -- patient FHIR ID
            
        Returns:
            patient_data {dict} --  patient data from Epic
        '''

        if not patient_id:
            print("No patient ID")
            return {}

        try:
            url = self.read_patient_url + patient_id
            
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            patient = {}

            xml = response.content
            tree = ElementTree.fromstring(xml)

            for element in tree.iter():
                # return the following dict {field : value} for the patient's information
                patient[element.tag.removeprefix("{http://hl7.org/fhir}")] = element.attrib.get('value')

            if not patient or patient.get('id') != patient_id:
                return {}

            return patient
        
        except Exception as e:
            print(f"Error getting patient data from epic. Status code: {response.status_code}: ", e)
            return {}


    def get_vitals(self, observation_id):
        '''Method to get patient vitals from Epic
        
        Args:
            observation_id {str} -- observation id from Epic
            
        Returns:
            vitals {dict} -- patient vitals from Epic
        '''

        if not observation_id:
            print("Invalid observation id")
            return None
        
        try:
            url = self.vitals_url + observation_id

            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            vitals = {}

            xml = response.content
            tree = ElementTree.fromstring(xml)

            for element in tree.iter():
                vitals[element.tag.removeprefix("{http://hl7.org/fhir}")] = element.attrib.get('value')

            return vitals
        
        except Exception as e:
            print(f"Error getting vitals from epic status code: {response.status_code}", e)


    def get_inactive_patients(self, patients):
        '''Method to get a list of patients in the database who are inactive
        
        Args:
            patient_mrns {list} -- list of patient instances 

        Returns:
            patient_ids {list} -- list of patients who are inactive
        '''
        inactive_patients = []
        for patient in patients:
            # call the get epic api to get the patient data based off of their mrn
            patient_data = self.get_patient(patient.patient_mrn)

            if patient_data.get('active') == "false":
                inactive_patients.append(patient)

        return inactive_patients


if __name__ == "__main__":
    epic = EpicAPIManager()
    # epic.search_patient(given="Lucas", family="Mitchell")
    # epic.search_patient(given="theodore", family="mychart", birthdate="1948-07-07")
    # print(epic.get_patient("T81lum-5p6QvDR7l6hv7lfE52bAbA2ylWBnv9CZEzNb0B"))
    print(epic.get_vitals("envjcVAhuFtXhXNFIg1Dr-2-8diVcq3BOMcZpbjYOC7JAJ1pPzK0v1075T4XMHL.83"))
    # print(epic.search_patient(_id="T81lum-5p6QvDR7l6hv7lfE52bAbA2ylWBnv9CZEzNb0B"))
    # e63wRTbPfr1p8UW81d8Seiw3
    # print(epic.search_patient(_id="e63wRTbPfr1p8UW81d8Seiw3"))
