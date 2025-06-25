# Have the models here (PATIENTS, DOCTORS, DEPARTMENTS, APPOINTMENTS, MEDICAL_RECORDS)
from app import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

class Doctor(db.Model, SerializerMixin):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    #department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    # Relationships
    #department = db.relationship('Department', back_populates='doctors')
    appointments = db.relationship('Appointment', back_populates='doctor', cascade='all, delete-orphan')
    #medical_records = db.relationship('Medical_record', back_populates='doctor', cascade='all, delete-orphan')

    serialize_rules = ('-appointments.doctor',) #'-department.doctors','-medical_records.doctor')

    def __repr__(self):
        return f"<Doctor {self.name}>"

class Appointment(db.Model, SerializerMixin):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)  # You can use db.DateTime if needed
    reason = db.Column(db.String, nullable=False)

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)

    # Relationships
    patient = db.relationship("Patient", back_populates="appointments")
    doctor = db.relationship("Doctor", back_populates="appointments")

    serialize_rules = ('-patient.appointments', '-doctor.appointments')

    def __repr__(self):
        return f"<Appointment {self.date} with Doctor {self.doctor_id}>"
    
class Patient(db.Model, SerializerMixin):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    admission_type = db.Column(db.String(50))  # e.g., 'Inpatient' or 'Outpatient'

    # Relationships
    appointments = db.relationship('Appointment', back_populates='patient', cascade='all, delete-orphan')
    #medical_records = db.relationship('Medical_record', back_populates='patient', cascade='all, delete-orphan')

    serialize_rules = ('-appointments.patient',) #'-medical_records.patient')

    def __repr__(self):
        return f"<Patient {self.name}>"

