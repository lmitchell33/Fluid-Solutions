from sqlalchemy import DateTime, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, relationship

Base = declarative_base()

# NOTE: these classes dont need initalizers becuase they are table models 
# for the database, if you want to set a default value then you could create an 
# initalizer and set the default value using kwargs 

class Patient(Base):
    __tablename__ = "Patient"

    id = mapped_column(Integer, primary_key=True)
    firstname = mapped_column(String)
    lastname = mapped_column(String)
    age = mapped_column(Integer, nullable=True)
    height_cm = mapped_column(Float, nullable=True)
    weight_kg = mapped_column(Float, nullable=True)
    patient_MRN = mapped_column(Integer, nullable=True)


    #NOTE: This is a one-to-many relationship as one patient can have many medications and many fluid instances
    # The first argument is the table the relationship corresponds with
    # The second argument is the attribute the relationship will correspond with on the other tables
    # The third argument specifies what type of cascading effect will be implemented when the patient is deleted 
    medications = relationship("Medication", back_populates="patient", cascade="all, delete-orphan")
    fluid_records = relationship("FluidRecords", back_populates="patient", cascade="all, delete-orphan")


class Medication(Base):
    __tablename__ = "Medications"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    dosage_mg = mapped_column(Float, nullable=True)
    frequency = mapped_column(Integer, nullable=True)

    #NOTE: This is a many-to-one relationship as there can be many medications per one patient
    patient_id = mapped_column(Integer, ForeignKey("Patient.id"))
    patient = relationship("Patient", back_populates="medications")


class FluidRecords(Base):
    __tablename__ = "FluidRecords"

    id = mapped_column(Integer, primary_key=True)
    fluid_given_time = mapped_column(DateTime)
    fluid_type = mapped_column(String)
    amount_ml = mapped_column(Float)

    #NOTE: This is a many-to-one relationship as there can be many fluid instances per one patient
    patient_id = mapped_column(Integer, ForeignKey("Patient.id"))
    patient = relationship("Patient", back_populates="fluid_records")
