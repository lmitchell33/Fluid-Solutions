import socket
import time
import random
from pyasn1.type import univ, namedtype
import datetime 

# ASN.1 Models for the data being sent
class BloodPressure(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('systolic', univ.Real()),
        namedtype.NamedType('diastolic', univ.Real())
    )

class VitalSigns(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('timestamp', univ.OctetString()),
        namedtype.NamedType('heartRate', univ.Real()),
        namedtype.NamedType('map', univ.Real()),
        namedtype.NamedType('ppv', univ.Real()),
        namedtype.NamedType('spo2', univ.Real()),
        namedtype.NamedType('bp', BloodPressure())
    )

def generate_mock_vitals():
    '''Generate mock vitals using whatever information we want'''
    # im thinking of creating a text file or csv with data we want to send then
    # randomly picking a row/set from that data and sending it as vitals info 

    return {"heart_rate":float(random.randint(0,10)), "map":float(random.randint(0,10)), 
            "cvp":float(random.randint(0,10)), "ppv":float(random.randint(0,10)), 
            "bp_sys":float(random.randint(0,10)), "bp_dias":float(random.randint(0,10)),
            "spo2":float(random.randint(0,10))}


def encode_vitals(data):
    vitals = VitalSigns()
    vitals.setComponentByName('timestamp', str(datetime.datetime.now()).encode())
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