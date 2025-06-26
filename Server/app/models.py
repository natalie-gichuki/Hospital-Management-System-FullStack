from app import db
from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

# ========================== USER ==========================
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-password_hash',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='patient')

    doctor = db.relationship('Doctor', back_populates='user', uselist=False)
    patient = db.relationship('Patient', back_populates='user', uselist=False)

    @property
    def password(self):
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @validates('username')
    def validate_username(self, key, username):
        if not username or len(username) < 4:
            raise ValueError("Username must be at least 4 characters.")
        return username

    @validates('role')
    def validate_role(self, key, role):
        valid_roles = ['admin', 'doctor', 'patient', 'department_manager']
        if role not in valid_roles:
            raise ValueError(f"Role must be one of {valid_roles}")
        return role

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


# ========================== PATIENT (POLYMORPHIC BASE) ==========================
class Patient(db.Model, SerializerMixin):
    __tablename__ = 'patients'
    serialize_rules = ('-appointments.patient', '-medical_records.patient', '-user.patient')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    type = db.Column(db.String, nullable=False, default='patient')

    date_of_birth = db.Column(db.Date)
    contact_number = db.Column(db.String(20), unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    user = db.relationship('User', back_populates='patient', uselist=False)

    appointments = db.relationship('Appointment', back_populates='patient', cascade="all, delete-orphan")
    medical_records = db.relationship('MedicalRecord', back_populates='patient', cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'patient',
        'polymorphic_on': type
    }

    def __repr__(self):
        return f"<Patient {self.name} ({self.type})>"


# ========================== INPATIENT ==========================
class Inpatient(Patient):
    __tablename__ = 'inpatients'

    id = db.Column(db.Integer, db.ForeignKey('patients.id'), primary_key=True)
    admission_date = db.Column(db.String, nullable=False)
    ward_number = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'inpatient'
    }


# ========================== OUTPATIENT ==========================
class Outpatient(Patient):
    __tablename__ = 'outpatients'

    id = db.Column(db.Integer, db.ForeignKey('patients.id'), primary_key=True)
    last_visit_date = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'outpatient'
    }


# ========================== DOCTOR ==========================
class Doctor(db.Model, SerializerMixin):
    __tablename__ = 'doctors'
    serialize_rules = ('-appointments.doctor', '-medical_records.doctor', '-user.doctor')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String)

    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)

    department = db.relationship(
        'Department',
        back_populates='doctors_in_department',
        foreign_keys=[department_id]
    )

    departments_headed = db.relationship(
        'Department',
        back_populates='head_doctor',
        foreign_keys='Department.head_doctor_id'
    )

    appointments = db.relationship('Appointment', back_populates='doctor', cascade="all, delete-orphan")
    medical_records = db.relationship('MedicalRecord', back_populates='doctor', cascade="all, delete-orphan")
    user = db.relationship('User', back_populates='doctor', uselist=False)

    def __repr__(self):
        return f"<Doctor {self.name}>"


# ========================== DEPARTMENT ==========================
class Department(db.Model, SerializerMixin):
    __tablename__ = 'departments'
    serialize_rules = ('-doctors_in_department.department',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    head_doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))

    doctors_in_department = db.relationship(
        'Doctor',
        back_populates='department',
        foreign_keys=[Doctor.department_id]
    )

    head_doctor = db.relationship(
        'Doctor',
        back_populates='departments_headed',
        foreign_keys=[head_doctor_id],
        post_update=True,
        uselist=False
    )


# ========================== APPOINTMENT ==========================
class Appointment(db.Model, SerializerMixin):
    __tablename__ = 'appointments'
    serialize_rules = ('-patient.appointments', '-doctor.appointments')

    id = db.Column(db.Integer, primary_key=True)
    appointment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String, default='Scheduled')  # Scheduled, Completed, Cancelled
    reason = db.Column(db.String, nullable=False)

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)

    patient = db.relationship('Patient', back_populates='appointments')
    doctor = db.relationship('Doctor', back_populates='appointments')

    def __repr__(self):
        return f"<Appointment on {self.appointment_date} with Doctor {self.doctor_id}>"


# ========================== MEDICAL RECORD ==========================
class MedicalRecord(db.Model, SerializerMixin):
    __tablename__ = 'medical_records'
    serialize_rules = ('-patient.medical_records', '-doctor.medical_records')

    id = db.Column(db.Integer, primary_key=True)
    diagnosis = db.Column(db.String, nullable=False)
    treatment = db.Column(db.String, nullable=False)
    visit_date = db.Column(db.DateTime, default=datetime.utcnow)

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)

    patient = db.relationship('Patient', back_populates='medical_records')
    doctor = db.relationship('Doctor', back_populates='medical_records')

    def __repr__(self):
        return f"<MedicalRecord {self.diagnosis} for Patient {self.patient_id}>"
