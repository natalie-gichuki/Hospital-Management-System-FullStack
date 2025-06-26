# app/models.py (updated version with User model and relationships)
from app import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-password_hash',) # Never serialize password hash

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='patient') # 'admin', 'doctor', 'patient', 'department_manager'

    # Relationships to existing models (optional, but good for linking)
    doctor = db.relationship('Doctor', back_populates='user', uselist=False)
    patient = db.relationship('Patient', back_populates='user', uselist=False)
    # department_manager_of = db.relationship('Department', back_populates='manager_user') # If a user manages a specific dept

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @validates('username')
    def validate_username(self, key, username):
        if not username or len(username) < 4:
            raise ValueError("Username must be at least 4 characters long.")
        return username

    @validates('role')
    def validate_role(self, key, role):
        valid_roles = ['admin', 'doctor', 'patient', 'department_manager']
        if role not in valid_roles:
            raise ValueError(f"Role must be one of {valid_roles}")
        return role

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"

# Modify Doctor model to link to User
class Doctor(db.Model, SerializerMixin):
    __tablename__ = 'doctors'
    serialize_rules = (
        '-department.doctors_in_department',
        '-department.head_doctor',
        '-departments_headed',
        '-appointments.doctor',
        '-medical_records.doctor',
        '-user.doctor' # Exclude back-reference
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=True) # New: Link to User
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)

    user = db.relationship('User', back_populates='doctor', uselist=False) # New: Relationship to User
    department = db.relationship('Department', back_populates='doctors_in_department', foreign_keys=[department_id])
    departments_headed = db.relationship('Department', back_populates='head_doctor', foreign_keys='Department.head_doctor_id')
    appointments = db.relationship('Appointment', back_populates='doctor', cascade="all, delete-orphan")
    medical_records = db.relationship('MedicalRecord', back_populates='doctor', cascade="all, delete-orphan")

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 2:
            raise ValueError("Doctor name must be at least 2 characters long.")
        return name

    @validates('specialization')
    def validate_specialization(self, key, specialization):
        if not specialization:
            raise ValueError("Specialization cannot be empty.")
        return specialization

    def __repr__(self):
        return f"<Doctor(id={self.id}, name='{self.name}', specialization='{self.specialization}')>"

# Modify Patient model to link to User
class Patient(db.Model, SerializerMixin):
    __tablename__ = 'patients'
    serialize_rules = ('-appointments.patient', '-medical_records.patient', '-user.patient') # Exclude back-reference

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=True) # New: Link to User
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    contact_number = db.Column(db.String(20), nullable=False, unique=True)

    user = db.relationship('User', back_populates='patient', uselist=False) # New: Relationship to User
    appointments = db.relationship('Appointment', back_populates='patient', cascade="all, delete-orphan")
    medical_records = db.relationship('MedicalRecord', back_populates='patient', cascade="all, delete-orphan")

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 2:
            raise ValueError("Patient name must be at least 2 characters long.")
        return name

    @validates('contact_number')
    def validate_contact_number(self, key, contact_number):
        if not contact_number or not contact_number.replace('+', '').isdigit() or len(contact_number) < 10:
            raise ValueError("Contact number must be a valid phone number with at least 10 digits.")
        return contact_number

    def __repr__(self):
        return f"<Patient(id={self.id}, name='{self.name}')>"

# Department model (no changes needed for linking to User directly for now, as 'department_manager' is a User role)
class Department(db.Model, SerializerMixin):
    __tablename__ = 'departments'
    serialize_rules = ('-doctors_in_department.department', '-head_doctor.departments_headed')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    specialty = db.Column(db.String(100), nullable=False)
    head_doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)

    doctors_in_department = db.relationship('Doctor', back_populates='department', foreign_keys='Doctor.department_id')
    head_doctor = db.relationship('Doctor', back_populates='departments_headed', foreign_keys=[head_doctor_id], uselist=False, post_update=True)

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 3:
            raise ValueError("Department name must be at least 3 characters long")
        return name

    @validates('specialty')
    def validate_specialty(self, key, specialty):
        if not specialty or len(specialty) < 3:
            raise ValueError("Department specialty must be at least 3 characters long")
        return specialty

    @validates('head_doctor_id')
    def validate_head_doctor_id(self, key, head_doctor_id):
        if head_doctor_id is None or not isinstance(head_doctor_id, int):
            raise ValueError("Head doctor ID must be a valid integer")
        return head_doctor_id

    def save(self, session):
        session.add(self)
        try:
            session.commit()
            return self
        except IntegrityError:
            session.rollback()
            raise ValueError("Department with this name already exists.")

    def delete(self, session):
        session.delete(self)
        session.commit()

    @classmethod
    def get_by_id(cls, session, department_id):
        return session.query(cls).filter_by(id=department_id).first()

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "specialty": self.specialty,
            "head_doctor_id": self.head_doctor_id,
            "head_doctor_name": self.head_doctor.name if self.head_doctor else None,
            "num_doctors_in_dept": len(self.doctors_in_department)
        }

class Appointment(db.Model, SerializerMixin):
    __tablename__ = 'appointments'
    serialize_rules = ('-patient.appointments', '-doctor.appointments')

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Scheduled')

    patient = db.relationship('Patient', back_populates='appointments')
    doctor = db.relationship('Doctor', back_populates='appointments')

    @validates('status')
    def validate_status(self, key, status):
        valid_statuses = ['Scheduled', 'Completed', 'Canceled']
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of {valid_statuses}")
        return status

    @validates('appointment_date')
    def validate_appointment_date(self, key, appointment_date):
        if appointment_date.replace(tzinfo=None) < datetime.utcnow():
            raise ValueError("Appointment date cannot be in the past.")
        return appointment_date

class MedicalRecord(db.Model, SerializerMixin):
    __tablename__ = 'medical_records'
    serialize_rules = ('-patient.medical_records', '-doctor.medical_records')

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    visit_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    diagnosis = db.Column(db.Text, nullable=False)
    treatment = db.Column(db.Text, nullable=False)

    patient = db.relationship('Patient', back_populates='medical_records')
    doctor = db.relationship('Doctor', back_populates='medical_records')

    @validates('diagnosis', 'treatment')
    def validate_text_fields(self, key, value):
        if not value or len(value) < 5:
            raise ValueError(f"{key.capitalize()} must be at least 5 characters long.")
        return value