from typing import List
from sqlalchemy import DateTime, Integer, String, Float, ForeignKey, Date 
from sqlalchemy.orm import mapped_column, relationship, Mapped, declarative_base

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patient"

    id = mapped_column(Integer, primary_key=True)
    firstname = mapped_column(String)
    lastname = mapped_column(String)
    dob = mapped_column(Date, nullable=True)
    gender = mapped_column(String, nullable=True)
    height_cm = mapped_column(Float, nullable=True)
    weight_kg = mapped_column(Float, nullable=True)
    patient_mrn = mapped_column(String, nullable=True, unique=True)

    # One-to-many relationship: One patient can have many medications or fluid records
    fluid_records: Mapped[List["FluidRecord"]] = relationship("FluidRecord", back_populates="patient", cascade="all, delete-orphan")


class FluidRecord(Base):
    __tablename__ = "fluid_record"

    id = mapped_column(Integer, primary_key=True)
    fluid_time_given = mapped_column(DateTime)
    amount_ml = mapped_column(Float)

    # Many-to-one relationship: Multiple fluid records can belong to one patient
    patient_id: Mapped[int] = mapped_column(Integer, ForeignKey("patient.id"))
    patient: Mapped["Patient"] = relationship("Patient", back_populates="fluid_records")

    # Many-to-one relationship: A fluid record is associated with one fluid type
    fluid_id: Mapped[int] = mapped_column(Integer, ForeignKey("fluid.id"))
    fluid: Mapped["Fluid"] = relationship("Fluid", back_populates="fluid_records", uselist=False)


class Fluid(Base):
    __tablename__ = "fluid"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, unique=True)

    # One-to-many relationship: A fluid type can have multiple associated fluid records
    fluid_records: Mapped[List["FluidRecord"]] = relationship("FluidRecord", back_populates="fluid")
