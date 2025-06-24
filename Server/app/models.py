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


class Inpatient(Patient):
    __tablename__ = 'inpatients'

    id = db.Column(db.Integer, db.ForeignKey('patients.id'), primary_key = True)
    admission_date = db.Column(db.String, nullable = False)
    ward_number = db.Column(db.Integer, nullable = False)

    __mapper_args__ = {
        'polymorphic_identity': 'inpatient',
    }


class Outpatient(Patient):
    pass