import socket
import time
import random
from datetime import datetime

from vitals_data_models import VitalSigns, BloodPressure, NumericObservation

def generate_mock_vitals():
    '''Generate mock vitals using whatever information we want'''
    # im thinking of creating a text file or csv with data we want to send then
    # randomly picking a row/set from that data and sending it as vitals info 

    return {"heart_rate":float(random.randint(0,10)), "map":float(random.randint(0,10)), 
            "cvp":float(random.randint(0,10)), "ppv":float(random.randint(0,10)), 
            "bp_sys":float(random.randint(0,10)), "bp_dias":float(random.randint(0,10)),
            "spo2":float(random.randint(0,10)), "timestamp":f"{datetime.now}"}


def encode_vitals(data):
    mdc_codes = {
        'timestamp' : f'{datetime.now()}',
        'heartRate' : '',
        'meanArterialPressure' : '',
        'pulsePressureVar' : '',
        'spo2' : '',
        'bloodPressure' : ''
    }

    # TODO: write this more algorithmicly
    vitals = VitalSigns()
    vitals.setComponentByName('timestamp', data.get('timestamp'))
    vitals.setComponentByName('heartRate', data.get('heart_rate'))
    vitals.setComponentByName('map', data.get('map'))
    vitals.setComponentByName('ppv', data.get('ppv'))
    vitals.setComponentByName('spo2', data.get('spo2'))

    bp = BloodPressure()
    bp.setComponentByName('systolic', data.get('bp_sys'))
    bp.setComponentByName('diastolic', data.get('bp_dias'))
    vitals.setComponentByName('bp', bp)
    
    encoded_data = vitals.prettyPrint()
    return encoded_data.encode()
    

def send_vitals(): 
    '''publish/send the vitals'''
    server = "host.docker.internal"
    port = 8080 

    vitals_agent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    vitals_agent.connect((server, port))

    try:
        while True:
            vitals_data = generate_mock_vitals()
            vitals_agent.sendall(encode_vitals(vitals_data))
            time.sleep(2)

    # stop gracefully
    except (ConnectionRefusedError, BrokenPipeError):
        print("Connection lost")
        vitals_agent.close()
    except KeyboardInterrupt:
        print("Stopping agent")
        vitals_agent.close()
    finally:
        vitals_agent.close()


if __name__ == "__main__":
    send_vitals()