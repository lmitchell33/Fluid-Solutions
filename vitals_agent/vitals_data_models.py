from pyasn1.type import univ, namedtype, char

class NumericObservation(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('mdcCode', univ.Integer()),  
        namedtype.NamedType('unitCode', univ.Integer()),
        namedtype.NamedType('value', univ.Integer())  
    )

class VitalSigns(univ.Sequence):
    componentType = namedtype.NamedTypes(
        namedtype.NamedType('timestamp', char.UTF8String()),
        namedtype.NamedType('heartRate', NumericObservation()),
        namedtype.NamedType('meanArterialPressure', NumericObservation()),
        namedtype.NamedType('spo2', NumericObservation()),
        namedtype.NamedType('respiratoryRate', NumericObservation()),
        namedtype.NamedType('systolicBP', NumericObservation()),
        namedtype.NamedType('diastolicBP', NumericObservation()),
    )