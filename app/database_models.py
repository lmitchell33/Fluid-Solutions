from typing import List
from sqlalchemy import DateTime, Integer, String, Float, ForeignKey, Date 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, relationship, Mapped

Base = declarative_base()

# NOTE: these classes dont need constructors becuase they are table models 
# for the database, if you want to set a default value then you could create an 
# constructor and set the default value using kwargs 

class Patient(Base):
    __tablename__ = "patient"

    id = mapped_column(Integer, primary_key=True)
    firstname = mapped_column(String)
    lastname = mapped_column(String)
    dob = mapped_column(Date, nullable=True)  # Used to find age
    height_cm = mapped_column(Float, nullable=True)
    weight_kg = mapped_column(Float, nullable=True)
    patient_mrn = mapped_column(Integer, nullable=True, unique=True)

    # One-to-many relationship: One patient can have many medications and fluid records
    medications: Mapped[List["Medication"]] = relationship("Medication", back_populates="patient", cascade="all, delete-orphan")
    fluid_records: Mapped[List["FluidRecord"]] = relationship("FluidRecord", back_populates="patient", cascade="all, delete-orphan")


class Medication(Base):
    __tablename__ = "medication"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    dosage_mg = mapped_column(Float, nullable=True)
    frequency = mapped_column(Integer, nullable=True)

    # Many-to-one relationship: Many medications can belong to one patient
    patient_id: Mapped[int] = mapped_column(Integer, ForeignKey("patient.id"))
    patient: Mapped["Patient"] = relationship("Patient", back_populates="medications")


class FluidRecord(Base):
    __tablename__ = "fluid_record"

    id = mapped_column(Integer, primary_key=True)
    fluid_time_given = mapped_column(DateTime)
    amount_ml = mapped_column(Float)

    # Many-to-one relationship: Many fluid records can belong to one patient
    patient_id: Mapped[int] = mapped_column(Integer, ForeignKey("patient.id"))
    patient: Mapped["Patient"] = relationship("Patient", back_populates="fluid_records")

    # Many-to-one relationship: One fluid record is associated with one fluid type
    fluid_id: Mapped[int] = mapped_column(Integer, ForeignKey("fluid.id"))
    fluid: Mapped["Fluid"] = relationship("Fluid", back_populates="fluid_records", uselist=False)


class Fluid(Base):
    __tablename__ = "fluid"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, unique=True)

    # One-to-one relationship: One fluid belongs to one fluid record
    fluid_records: Mapped[List["FluidRecord"]] = relationship("FluidRecord", back_populates="fluid")
