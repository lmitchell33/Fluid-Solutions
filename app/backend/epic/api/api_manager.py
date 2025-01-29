import os
import requests
import time
from xml.etree import ElementTree
from threading import Lock

from backend.epic.auth.auth import get_access_token, create_jwt
# from auth.auth import get_access_token, create_jwt

class EpicAPIManager:
    '''Singleton class to manage the Epic API requests. 
    
    Properties:
        access_token {str} -- access token for the Epic API session. Typically valid for 3600 seconsd.

    Methods:
        search_patient(**kwargs) - Search for patient ID and information from Epic
        get_patient_data(patient_id) -- get patient data from Epic 
        get_patient_vitals(observation_id) -- get patient vitals from Epic
    '''
    _instance = None
    _lock = Lock()

    def __new__(cls):
        '''Ensure only one instance of class is created, following the Singleton pattern'''
        if not cls._instance:
            with cls._lock:
                cls._instance = super(EpicAPIManager, cls).__new__(cls)
                cls._instance._initalized = False
        
        return cls._instance
    
    def __init__(self):
        '''Initialize the API Manager, ensuring initialization is done only once.'''
        if self._initalized:
            return
        
        self._initalized = True

        # urls for each of the Epic API endpoints we are using
        self.search_patient_url = os.environ.get("SEARCH_PATIENT_URL")
        self.vitals_url = os.environ.get("READ_VITALS_URL")
        self.read_patient_url = os.environ.get("READ_PATIENT_URL")

        # private variables to hold auth information for the session
        self._jwt = create_jwt()  # jwt for the session
        self._access_token = None # access token for the session
        self._access_token_expr = None # expiration time for the access token

        # specify the headers for each request
        self.headers = {
            "Authorization" : f"Bearer {self.access_token}",
            "Content-Type" : "application/json"
        }


    @property
    def access_token(self):
        '''Property of the class to get the access token and ensure its not expired'''
        
        # check if the token is expired and get a new one if it is
        if (not self._access_token) or (time.time() >= self._access_token_expr):
            self._get_new_access_token() 
        
        return self._access_token


    def _get_new_access_token(self):
        '''Private method to get a new access token from Epic'''
        if not self._jwt:
            self._jwt = create_jwt()
        
        epic_auth_response = get_access_token(self._jwt)

        # parse epic's OAuth endpoint response to get the info we need
        self._access_token = epic_auth_response["access_token"]
        self._access_token_expr = time.time() + epic_auth_response["expires_in"]


    def search_patient(self, **kwargs):
        '''Method to search Epic for a patient
        
        Kwargs:
            **kwargs {dict} -- search parameters for the patient. A list of valid parameters is shown below
                - address
                - address_city
                - address_postalcode
                - address_state
                - birthdate
                - family
                - gender
                - given
                - identifier
                - legal_sex
                - own_name
                - own_prefix
                - partner_name
                - partner_prefix
                - telecom

        Returns:
            patient_data {str} -- patient data from Epic        
        '''

        # NOTE: Becuase we are using a sandbox and we dont have our own patient data
        # with our own server, I cant find a set of parameters that will allow us to
        # get a valid response (find a patient). 

        # Define the allowed search parameters for the API (from Epic)
        allowed_keys = [
            "address", "address_city", "address_postalcode", "address_state",
            "birthdate", "family", "gender", "given", "identifier",
            "legal_sex", "own_name", "own_prefix", "partner_name",
            "partner_prefix", "telecom"
        ]
    
        # filter for the kwargs so that only the valid serach parameters are used
        payload = {k.replace('_', '-'): v for k, v in kwargs.items() if k in allowed_keys}

        response = requests.get(self.search_patient_url, payload, headers=self.headers)

        # check the response is valid before proceeding
        if 200 <= response.status_code < 300:
            # TODO: Implement logic for integration here
            xml = response.content
            tree = ElementTree.fromstring(xml)

            for element in tree.iter():
                print(element.tag.removeprefix("{http://hl7.org/fhir}"), element.attrib)
        
        else:
            print(f"Bad Response: {response.status_code}")


    def get_patient_data(self, patient_id):
        '''Method to get patient data from Epic
        
        Args:
            patient_id {str} -- patient FHIR ID
            
        Returns:
            patient_data {dict} --  patient data from Epic
        '''

        if not patient_id:
            print("No patient ID")
            return {}

        url = self.read_patient_url + patient_id

        response = requests.get(url, headers=self.headers)

        patient = {}

        # check the response is valid before proceeding
        if 200 <= response.status_code < 300:
            # TODO: Implement logic for integration here
            xml = response.content
            tree = ElementTree.fromstring(xml)

            for element in tree.iter():
                print(element.tag.removeprefix("{http://hl7.org/fhir}"), element.attrib)
        
                patient[element.tag.removeprefix("{http://hl7.org/fhir}")] = element.attrib.get('value')

        else:
            print(f"Bad Response: {response.status_code}")
            
        return patient


    def get_patient_vitals(self, observation_id):
        '''Method to get patient vitals from Epic
        
        Args:
            observation_id {str} -- observation id from Epic
            
        Returns:
            vitals {dict} -- patient vitals from Epic
        '''

        url = self.vitals_url + observation_id

        response = requests.get(url, headers=self.headers)

        # check the response is valid before proceeding
        if 200 <= response.status_code < 300:
            # TODO: Implement logic for integration here
            xml = response.content
            tree = ElementTree.fromstring(xml)

            for element in tree.iter():
                print(element.tag.removeprefix("{http://hl7.org/fhir}"), element.attrib)
        
        else:
            print(f"Bad Response: {response.status_code}")


    def get_inactive_patients(self, patients):
        '''Method to get a list of patients in the database who are inactive
        
        Args:
            patient_mrns {list} -- list of patient instances 

        Returns:
            patient_ids {list} -- list of patient MRN's who are inactive
        '''
        inactive_patients = []
        for patient in patients:
            patient_data = self.get_patient_data(patient.patient_mrn)

            if patient_data.get('active') == "false":
                inactive_patients.append(patient)

        return inactive_patients


if __name__ == "__main__":
    epic = EpicAPIManager()
    # epic.search_patient(own_name="theodore")
    epic.get_patient_data("T81lum-5p6QvDR7l6hv7lfE52bAbA2ylWBnv9CZEzNb0B")
    # epic.get_patient_vitals("envjcVAhuFtXhXNFIg1Dr-2-8diVcq3BOMcZpbjYOC7JAJ1pPzK0v1075T4XMHL.83")
    