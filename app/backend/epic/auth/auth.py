from base64 import urlsafe_b64encode
from cryptography.x509 import load_pem_x509_certificate
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

import jwt
import requests
import uuid
import os

# load in the secrets from the .env file
load_dotenv()

# get the client secrets and credentials
CLIENT_ID = os.getenv("CLIENT_ID")
NON_PRODUCTION_CLIENT_ID = os.getenv("NON_PRODUCTION_CLIENT_ID")
TOKEN_URL = os.getenv("TOKEN_URL")

# generate a unique key id number to be used for the JWT token and set
kid = str(uuid.uuid4())

def get_public_key_modulus(key_file):
    '''Find the modulus of a x509 public key (certificate)
    
    Args: 
        key_file {str} -- path to the x509 public key file

    Returns:
        base64_modulus {str} -- the base64 encoded modulus of the public key
    '''

    # Load the certificate
    with open(key_file, "rb") as cert_file:
        cert_data = cert_file.read()

    # Parse the certificate
    certificate = load_pem_x509_certificate(cert_data)

    # Extract the public key from the certificate
    public_key = certificate.public_key()

    # Extract the modulus and exponent
    numbers = public_key.public_numbers()
    modulus = numbers.n

    # Convert modulus and exponent to base64 URL
    base64_modulus = urlsafe_b64encode(modulus.to_bytes((modulus.bit_length() + 7) // 8, byteorder='big')).decode('utf-8').rstrip('=')

    return base64_modulus


def create_jwt():
    '''Create a JWT token for the OAuth 2.0 backend server workflow, based on Epic documentation'''
    jti = str(uuid.uuid4())
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=4.5) # must be 5 minutes or less

    # JWT headers and payload, as required by Epic
    jwt_headers = {"kid" : kid}
    jwt_payload = {
        'iss' : NON_PRODUCTION_CLIENT_ID,
        'sub' : NON_PRODUCTION_CLIENT_ID,
        'aud' : TOKEN_URL,
        'jti' : jti,
        'exp' : int(expiration_time.timestamp())
    }

    # load the private key
    with open("./backend/epic/auth/keys/privatekey.pem", "r") as key:
        private_key = key.read()

    # create the token
    json_web_token = jwt.encode(payload=jwt_payload, key=private_key, algorithm='RS256', headers=jwt_headers)

    return json_web_token


def get_access_token(jwt=None):
    '''Requests and receives an access token from Epic using the Backend Server model
    
    Kwargs:
        jwt {jwt} - json web token to be used for the request
        
    Returns:
        access_token {str} -- access token for the Epic APIs
    '''

    if not jwt:
        jwt = create_jwt()
 
    # OAuth 2.0 http request information
    auth_headers = {
        'Content-Type' : "application/x-www-form-urlencoded"
    }

    auth_payload = {
        "grant_type" : "client_credentials",
        "client_assertion_type" : "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion" : jwt
    }

    try: 
        response = requests.post(url=TOKEN_URL, data=auth_payload, headers=auth_headers)
        return response.json()
    except requests.exceptions.MissingSchema as e:
        print(f"Could not get access token, {e}")
        return None


if __name__ == "__main__":
    json_web_token = create_jwt()
    token = get_access_token(json_web_token)
    print(token)

    # Testing URL to make sure the Epic servers is up 
    # response = requests.get("https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/.well-known/smart-configuration")s
    # print(response.headers, response.reason)
