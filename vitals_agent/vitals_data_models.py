from pyasn1.type import univ, namedtype

class NumericObservation(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('mdcCode', univ.ObjectIdentifier()),
        namedtype.NamedType('unitCode', univ.ObjectIdentifier()),
        namedtype.NamedType('value', univ.Integer())
    )

class BloodPressure(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('systolic', NumericObservation),
        namedtype.NamedType('diastolic', NumericObservation)
    )

class VitalSigns(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('timestamp', univ.OctetString()),
        namedtype.NamedType('heartRate', NumericObservation),
        namedtype.NamedType('map', NumericObservation),
        namedtype.NamedType('ppv', NumericObservation),
        namedtype.NamedType('spo2', NumericObservation),
        namedtype.NamedType('bp', BloodPressure())
    )

