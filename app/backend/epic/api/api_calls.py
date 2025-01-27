import os
import requests
import time
from xml.etree import ElementTree
from auth.auth import get_access_token, create_jwt

class EpicAPI:
    '''
    Maybe do use a class like this to hold the expirtaion for the auth token??
    '''
    def __init__(self):
        # urls for each of the Epic API endpoints we are using
        self.search_patient_url = os.environ.get("SEARCH_PATIENT_URL")
        self.vitals_url = os.environ.get("READ_VITALS_URL")
        self.read_patient_url = os.environ.get("READ_PATIENT_URL")
        
        # private variables to hold auth information for the session
        self._jwt = create_jwt()  # jwt for the session
        self._access_token = None # access token for the session
        self._access_token_expr = None # expiration time for the access token


    def _get_new_access_token(self):
        '''Private method to get a new access token from Epic'''
        if not self._jwt:
            self._jwt = create_jwt()
        
        epic_auth_response = get_access_token(self._jwt)

        # parse epic's OAuth endpoint response to get the info we need
        self._access_token = epic_auth_response["access_token"]
        self._access_token_expr = time.time() + epic_auth_response["expires_in"]


    @property
    def access_token(self):
        '''Property of the class to get the access token and ensure its not expired'''
        
        # check if the token is expired and get a new one if it is
        if not self._access_token or time.time() >= self._access_token_expr:
            self._get_new_access_token() 
        
        return self._access_token


    # TODO: update the parameters here
    def search_patient(self, **Kwargs):
        '''Method to search Epic for a patient'''

        # required information for the requst
        payload = {
            "address-city" : "Erie",
            "address-state" : "Pennsylvania",
            "gender" : "Male",
            "address" : "5947 Southland Drive",
            "own-name" : "Lucas Mitchell"
        }

        headers = {
            "Authorization" : f"Bearer {self.access_token}"
        }

        response = requests.get(self.search_patient_url, payload, headers=headers)

        # check the response is valid before proceeding
        if 200 <= response.status_code < 300:
            # TODO: Implement logic for integration here
            xml = response.content
            tree = ElementTree.fromstring(xml)

            for element in tree.iter():
                print(element.tag, element.attrib)


    def get_patient_data(self, patient_id):
        '''Method to get patient data from Epic
        
        Args:
            patient_id {str} -- patient FHIR ID
            
        Returns:
            patient_data {dict} --  patient data from Epic
        '''

        url = self.read_patient_url + patient_id

        headers = {
            "Authorization" : f"Bearer {self.access_token}",
            "Content-Type" : "application/json"
        }

        response = requests.get(url, headers=headers)

        # check the response is valid before proceeding
        if 200 <= response.status_code < 300:
            # TODO: Implement logic for integration here
            xml = response.content
            tree = ElementTree.fromstring(xml)

            for element in tree.iter():
                print(element.tag, element.attrib)


    def get_patient_vitals(self, observation_id):
        headers = {
            "Authorization" : f"Bearer {self.access_token}",
            "Content-Type" : "application/json"
        }

        url = self.vitals_url + observation_id

        response = requests.get(url, headers=headers)

        # check the response is valid before proceeding
        if 200 <= response.status_code < 300:
            # TODO: Implement logic for integration here
            xml = response.content
            tree = ElementTree.fromstring(xml)

            for element in tree.iter():
                print(element.tag, element.attrib)


if __name__ == "__main__":
    epic = EpicAPI()
    # epic.search_patient()
    # epic.get_patient_data("T81lum-5p6QvDR7l6hv7lfE52bAbA2ylWBnv9CZEzNb0B")
    epic.get_patient_vitals("envjcVAhuFtXhXNFIg1Dr-2-8diVcq3BOMcZpbjYOC7JAJ1pPzK0v1075T4XMHL.83")