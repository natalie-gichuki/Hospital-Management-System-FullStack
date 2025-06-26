# Have the models here (PATIENTS, DOCTORS, DEPARTMENTS, APPOINTMENTS, MEDICAL_RECORDS)
from app import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

class Doctor(db.Model, SerializerMixin):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    specialization = db.Column(db.String, nullable=False)

    medical_records = db.relationship('Medical_Record', back_populates='doctor', cascade='all, delete-orphan')
    headed_departments = db.relationship('Department', back_populates='head_doctor', cascade='all, delete-orphan')

    serialize_rules = ('-medical_records.doctor', '-headed_departments.head_doctor',)


class Department(db.Model, SerializerMixin):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    specialty = db.Column(db.String, nullable=False)
    headdoctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=True)

    head_doctor = db.relationship('Doctor', back_populates='headed_departments', foreign_keys=[headdoctor_id])

    serialize_rules = ('-head_doctor.headed_departments',)
