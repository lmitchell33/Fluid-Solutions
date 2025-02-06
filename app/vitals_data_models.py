from pyasn1.type import univ, namedtype

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