# Have the models here (PATIENTS, DOCTORS, DEPARTMENTS, APPOINTMENTS, MEDICAL_RECORDS)
from app import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates



class Patient(db.Model, SerializerMixin):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    age = db.Column(db.Integer, nullable = False)
    gender = db.Column(db.String, nullable = False)
    type = db.Column(db.String, nullable = False)

    __mapper_args__ = {
        'polymorphic_identity': 'patient',
        'polymorphic_on': type
    }

    medical_records = db.relationship('Medical_Record', back_populates='patient', cascade='all, delete-orphan')
    appointments = db.relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")

    serialize_rules = (
    '-appointments.patient',
    '-appointments.doctor.appointments',
    '-medical_records.patient',
    '-medical_records.doctor.medical_records'
   )




class Inpatient(Patient):
    __tablename__ = 'inpatients'

    id = db.Column(db.Integer, db.ForeignKey('patients.id'), primary_key = True)
    admission_date = db.Column(db.String, nullable = False)
    ward_number = db.Column(db.Integer, nullable = False)

    __mapper_args__ = {
        'polymorphic_identity': 'inpatient',
    }


class Outpatient(Patient):
    __tablename__ = 'outpatient'

    id = db.Column(db.Integer, db.ForeignKey('patients.id'), primary_key=True)
    last_visit_date = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'outpatient',
    }


class Medical_Record(db.Model, SerializerMixin):
    __tablename__ = 'medical_records'

    
    serialize_rules = (
    '-patient.medical_records',
    '-doctor.medical_records',
    '-patient.appointments',
    '-doctor.appointments'
)


    id = db.Column(db.Integer, primary_key = True)
    diagnosis = db.Column(db.String, nullable = False)
    treatment = db.Column(db.String, nullable = False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable = False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable = False)
    date = db.Column(db.String, nullable = False) 


    patient = db.relationship('Patient', back_populates='medical_records')
    doctor = db.relationship('Doctor', back_populates='medical_records')



class Doctor(db.Model, SerializerMixin):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String)
    #department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    # Relationships
    #department = db.relationship('Department', back_populates='doctors')
    appointments = db.relationship('Appointment', back_populates='doctor', cascade='all, delete-orphan')
    medical_records = db.relationship('Medical_Record', back_populates='doctor', cascade='all, delete-orphan')

    serialize_rules = (
    '-appointments.doctor',
    '-appointments.patient.appointments',
    '-medical_records.doctor',
    '-medical_records.patient.medical_records'
)

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

    serialize_rules = (
    '-patient.appointments',
    '-doctor.appointments',
    '-patient.medical_records',
    '-doctor.medical_records'
)


    def __repr__(self):
        return f"<Appointment {self.date} with Doctor {self.doctor_id}>"
    
