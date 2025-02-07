import socket
import time
import random
from datetime import datetime

from pyasn1.codec.der.encoder import encode

from vitals_data_models import VitalSigns, NumericObservation


def generate_mock_vitals():
    '''Generate mock vitals using whatever information we want'''

    return {
        "heartRate":random.randint(0,10), 
        "meanArterialPressure":random.randint(0,10), 
        "cvp":random.randint(0,10), 
        "pulsePressureVar":random.randint(0,10), 
        "systolicBP":f'{random.randint(0,10)}', 
        "diastolicBP" : f'{random.randint(0,10)}',
        "spo2":random.randint(0,10), 
        "timestamp":f"{datetime.now().isoformat()}"
    }


def encode_vitals(data):

    # These mdc_codes could be wrong, but im not paying for the document to find out
    mdc_codes = {
        'timestamp': {'mdcCode': None, 'unitCode': None},  # No MDC code for timestamp
        'heartRate': {'mdcCode': 18402, 'unitCode': 264864},  # MDC_PULS_RATE (bpm)
        'meanArterialPressure': {'mdcCode': 18949, 'unitCode': 266016},  # MDC_PRESS_BLD_ART_MEAN (mmHg)
        'pulsePressureVar': {'mdcCode': 18951, 'unitCode': 266016},  # MDC_PRESS_BLD_ART_PULS (mmHg)
        'spo2': {'mdcCode': 150456, 'unitCode': 262144},  # MDC_PULS_OXIM_SAT_O2 (percentage)
        'cvp': {'mdcCode': 18945, 'unitCode': 266016},  # MDC_PRESS_CVP (mmHg)
        'systolicBP': {'mdcCode': 18947, 'unitCode': 266016},  # MDC_PRESS_BLD_ART_SYS (mmHg)
        'diastolicBP': {'mdcCode': 18948, 'unitCode': 266016}  # MDC_PRESS_BLD_ART_DIA (mmHg)
    }


    raw_data = VitalSigns()

    for key, value in data.items():
        if key == 'timestamp':
            raw_data.setComponentByName(key, value)
            continue

        observation_component = NumericObservation()

        # add the mdc and unit codes to the NumericOvservation
        for field, field_value in mdc_codes.get(key).items():
            observation_component.setComponentByName(f"{field}", field_value)

        # add the value to the NumericObservation
        observation_component.setComponentByName('value', f"{value}")
        
        # add the NumericObservation to the final message to be transmitted
        raw_data.setComponentByName(key, observation_component)
    
    # encode and return the vitals data
    return encode(raw_data)
    

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