# models.py
from app import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint # Can be used for more complex column-level constraints if needed
from datetime import datetime, date # Import both datetime and date for appropriate column types
from werkzeug.security import generate_password_hash, check_password_hash # For password hashing


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False) # Stores the hashed password
    role = db.Column(db.String(50), nullable=False) # e.g., 'doctor', 'patient', 'admin'

    # Relationships (one-to-one with Doctor and Patient profiles)
    # uselist=False indicates a one-to-one relationship
    doctor_profile = db.relationship('Doctor', back_populates='user', uselist=False, cascade='all, delete-orphan')
    patient_profile = db.relationship('Patient', back_populates='user', uselist=False, cascade='all, delete-orphan')

    # Do not serialize the password hash for security
    serialize_rules = ('-_password_hash',)

    # Getter for password (raises AttributeError to prevent direct access)
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # Setter for password (hashes the password before storing)
    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    # Method to verify password
    def verify_password(self, password):
        return check_password_hash(self._password_hash, password)

    # Validations for User model fields
    @validates('username')
    def validate_username(self, key, username):
        if not username or not isinstance(username, str) or len(username.strip()) == 0:
            raise ValueError("Username must be a non-empty string.")
        # Optional: Check for uniqueness at the validation level (unique=True handles it at DB level)
        # if User.query.filter_by(username=username).first():
        #     raise ValueError("Username already exists.")
        return username.strip()

    @validates('role')
    def validate_role(self, key, role):
        normalized_role = role.lower().strip()
        if normalized_role not in ['doctor', 'patient', 'admin']:
            raise ValueError("Role must be 'doctor', 'patient', or 'admin'.")
        return normalized_role

    def __repr__(self):
        return f"<User {self.id}: {self.username} (Role: {self.role})>"


class Patient(db.Model, SerializerMixin):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    # 'type' is the discriminator column for polymorphic loading in single table inheritance
    type = db.Column(db.String(50), nullable=False)

    # Foreign key to User model for one-to-one relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    user = db.relationship('User', back_populates='patient_profile')

    __mapper_args__ = {
        'polymorphic_identity': 'patient',
        'polymorphic_on': type
    }

    # Relationships to other models
    medical_records = db.relationship('Medical_Record', back_populates='patient', cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', back_populates='patient', cascade='all, delete-orphan')

    # Serialization rules to prevent circular references when returning JSON
    serialize_rules = (
        '-medical_records.patient',  # Do not serialize patient from within medical_records
        '-appointments.patient',     # Do not serialize patient from within appointments
        '-user.patient_profile',     # Do not serialize patient_profile from User
    )

    # Data validation using SQLAlchemy's @validates decorator
    @validates('name')
    def validate_name(self, key, name):
        if not name or not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Name must be a non-empty string.")
        return name.strip()

    @validates('age')
    def validate_age(self, key, age):
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Age must be a positive integer.")
        return age

    @validates('gender')
    def validate_gender(self, key, gender):
        # Normalize gender to lowercase and check against allowed values
        normalized_gender = gender.lower().strip()
        if normalized_gender not in ['male', 'female', 'other']:
            raise ValueError("Gender must be 'male', 'female', or 'other'.")
        return normalized_gender

    def __repr__(self):
        return f"<Patient {self.id}: {self.name} (Age: {self.age}, Gender: {self.gender}, Type: {self.type})>"


class Inpatient(Patient):
    __tablename__ = 'inpatients'

    # Foreign key relationship to the Patient table, making it a child of Patient
    id = db.Column(db.Integer, db.ForeignKey('patients.id'), primary_key=True)
    # Using db.Date for date fields for proper date handling and querying
    admission_date = db.Column(db.Date, nullable=False)
    ward_number = db.Column(db.Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'inpatient',
    }

    # Validations specific to Inpatient
    @validates('ward_number')
    def validate_ward_number(self, key, ward_number):
        if not isinstance(ward_number, int) or ward_number <= 0:
            raise ValueError("Ward number must be a positive integer.")
        return ward_number

    @validates('admission_date')
    def validate_admission_date(self, key, admission_date):
        if not isinstance(admission_date, date): # Use date, not datetime for db.Date columns
            raise ValueError("Admission date must be a valid date object.")
        return admission_date

    def __repr__(self):
        return f"<Inpatient {self.id}: Ward {self.ward_number}, Admitted: {self.admission_date}>"


class Outpatient(Patient):
    __tablename__ = 'outpatients' # Corrected typo: 'outpatient' -> 'outpatients'

    # Foreign key relationship to the Patient table
    id = db.Column(db.Integer, db.ForeignKey('patients.id'), primary_key=True)
    # Using db.Date for date fields
    last_visit_date = db.Column(db.Date, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'outpatient',
    }

    # Validations specific to Outpatient
    @validates('last_visit_date')
    def validate_last_visit_date(self, key, last_visit_date):
        if not isinstance(last_visit_date, date): # Use date, not datetime for db.Date columns
            raise ValueError("Last visit date must be a valid date object.")
        return last_visit_date

    def __repr__(self):
        return f"<Outpatient {self.id}: Last Visit: {self.last_visit_date}>"


class Doctor(db.Model, SerializerMixin):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    # Contact can be phone or email; added unique constraint for contact
    contact = db.Column(db.String(100), unique=True, nullable=True) # Made nullable as contact might not always be available

    # Foreign key to Department
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    # Foreign key to User model for one-to-one relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    # Relationships
    department = db.relationship('Department', back_populates='doctors')
    appointments = db.relationship('Appointment', back_populates='doctor', cascade='all, delete-orphan')
    medical_records = db.relationship('Medical_Record', back_populates='doctor', cascade='all, delete-orphan')
    user = db.relationship('User', back_populates='doctor_profile') # Relationship to User model

    # Serialization rules to prevent circular references
    serialize_rules = (
        '-appointments.doctor',
        '-medical_records.doctor',
        '-department.doctors', # Prevent endless loop if Department also serializes its doctors
        '-user.doctor_profile', # Do not serialize doctor_profile from User
    )

    # Validations for Doctor model fields
    @validates('name')
    def validate_name(self, key, name):
        if not name or not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Doctor name must be a non-empty string.")
        return name.strip()

    @validates('specialization')
    def validate_specialization(self, key, specialization):
        if not specialization or not isinstance(specialization, str) or len(specialization.strip()) == 0:
            raise ValueError("Specialization must be a non-empty string.")
        return specialization.strip()

    @validates('contact')
    def validate_contact(self, key, contact):
        if contact is not None:
            if not isinstance(contact, str):
                raise ValueError("Contact must be a string or None.")
            if len(contact.strip()) < 5: # Basic length check
                 raise ValueError("Contact information appears too short or invalid.")
            return contact.strip()
        return None

    def __repr__(self):
        return f"<Doctor {self.id}: {self.name} ({self.specialization})>"


class Department(db.Model, SerializerMixin):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    # headdoctor_id can be null if a department temporarily has no head doctor
    headdoctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), unique=True, nullable=True)

    # Relationships
    # One-to-many: Department has many Doctors
    doctors = db.relationship('Doctor', back_populates='department', cascade='all, delete-orphan')
    # One-to-one: Department has one Head Doctor (explicitly linked by foreign_keys)
    # post_update=True handles potential circular dependency on updates (e.g., if headdoctor also has a department_id)
    headdoctor = db.relationship('Doctor', foreign_keys=[headdoctor_id], post_update=True)

    serialize_rules = (
        '-doctors.department',      # Prevent circular reference: doctors should not serialize their department back
        '-headdoctor.department'    # Prevent circular reference for the head doctor relationship
    )

    # Validations for Department model fields
    @validates('name')
    def validate_name(self, key, name):
        if not name or not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Department name must be a non-empty string.")
        return name.strip()

    @validates('specialty')
    def validate_specialty(self, key, specialty):
        if not specialty or not isinstance(specialty, str) or len(specialty.strip()) == 0:
            raise ValueError("Department specialty must be a non-empty string.")
        return specialty.strip()

    def __repr__(self):
        return f"<Department {self.id}: {self.name} ({self.specialty})>"


class Appointment(db.Model, SerializerMixin):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    # Using db.DateTime for precise date and time of appointment
    date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255), nullable=False) # Added length for reason
    status = db.Column(db.String(50), nullable=False, default='Scheduled') # Added status

    # Foreign keys
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)

    # Relationships
    patient = db.relationship("Patient", back_populates="appointments")
    doctor = db.relationship("Doctor", back_populates="appointments")

    serialize_rules = (
        '-patient.appointments', # Prevent circular reference for patient's appointments
        '-doctor.appointments'   # Prevent circular reference for doctor's appointments
    )

    # Validations for Appointment model fields
    @validates('date')
    def validate_date(self, key, date_obj): # Renamed 'date' parameter to avoid conflict with column name
        if not isinstance(date_obj, datetime):
            raise ValueError("Appointment date must be a valid datetime object.")
        # Example: Ensure appointment is not in the past
        # if date_obj < datetime.now():
        #     raise ValueError("Appointment date cannot be in the past.")
        return date_obj

    @validates('reason')
    def validate_reason(self, key, reason):
        if not reason or not isinstance(reason, str) or len(reason.strip()) < 5:
            raise ValueError("Reason must be a descriptive string of at least 5 characters.")
        return reason.strip()

    @validates('status')
    def validate_status(self, key, status):
        normalized_status = status.lower().strip()
        if normalized_status not in ['scheduled', 'completed', 'cancelled']:
            raise ValueError("Status must be 'Scheduled', 'Completed', or 'Cancelled'.")
        return normalized_status.capitalize() # Store with first letter capitalized

    def __repr__(self):
        return f"<Appointment {self.id} on {self.date.strftime('%Y-%m-%d %H:%M')} for Patient {self.patient_id} with Doctor {self.doctor_id} (Status: {self.status})>"


class Medical_Record(db.Model, SerializerMixin):
    __tablename__ = 'medical_records'

    id = db.Column(db.Integer, primary_key=True)
    diagnosis = db.Column(db.String(255), nullable=False)
    treatment = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False) # Using db.DateTime for recording medical record date/time

    # Foreign keys
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)

    # Relationships
    patient = db.relationship('Patient', back_populates='medical_records')
    doctor = db.relationship('Doctor', back_populates='medical_records')

    serialize_rules = (
        '-patient.medical_records', # Prevent circular reference for patient's medical records
        '-doctor.medical_records'   # Prevent circular reference for doctor's medical records
    )

    # Validations for Medical_Record model fields
    @validates('diagnosis')
    def validate_diagnosis(self, key, diagnosis):
        if not diagnosis or not isinstance(diagnosis, str) or len(diagnosis.strip()) < 5:
            raise ValueError("Diagnosis must be a descriptive string of at least 5 characters.")
        return diagnosis.strip()

    @validates('treatment')
    def validate_treatment(self, key, treatment):
        if not treatment or not isinstance(treatment, str) or len(treatment.strip()) < 5:
            raise ValueError("Treatment must be a descriptive string of at least 5 characters.")
        return treatment.strip()

    @validates('date')
    def validate_date(self, key, date_obj): # Renamed 'date' parameter
        if not isinstance(date_obj, datetime):
            raise ValueError("Medical record date must be a valid datetime object.")
        return date_obj

    def __repr__(self):
        return f"<Medical Record {self.id} for Patient {self.patient_id} by Doctor {self.doctor_id} on {self.date.strftime('%Y-%m-%d %H:%M')}>"