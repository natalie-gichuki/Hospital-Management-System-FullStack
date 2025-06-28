# models.py
from app import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint # Not used in current validates, but good to have if needed for column constraints
from datetime import datetime # Import datetime for date validations and default values


class Patient(db.Model, SerializerMixin):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # Added length for string
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(50), nullable=False) # Added length for string
    # 'type' is the discriminator column for polymorphic loading
    type = db.Column(db.String(50), nullable=False) # Added length for string

    __mapper_args__ = {
        'polymorphic_identity': 'patient',
        'polymorphic_on': type
    }

    # Relationships
    medical_records = db.relationship('Medical_Record', back_populates='patient', cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', back_populates='patient', cascade='all, delete-orphan')

    # Serialization rules to prevent circular references when returning JSON
    serialize_rules = (
        '-medical_records.patient',  # Do not serialize patient from within medical_records
        '-appointments.patient',     # Do not serialize patient from within appointments
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
        # Representation for easier debugging
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

    @validates('ward_number')
    def validate_ward_number(self, key, ward_number):
        if not isinstance(ward_number, int) or ward_number <= 0:
            raise ValueError("Ward number must be a positive integer.")
        return ward_number

    @validates('admission_date')
    def validate_admission_date(self, key, admission_date):
        if not isinstance(admission_date, (datetime, type(None))): # Allow None if column was nullable, but it's not here
            raise ValueError("Admission date must be a valid date object.")
        # Optional: Add logic to ensure date is not in the future, etc.
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

    @validates('last_visit_date')
    def validate_last_visit_date(self, key, last_visit_date):
        if not isinstance(last_visit_date, (datetime, type(None))): # Allow None if column was nullable
            raise ValueError("Last visit date must be a valid date object.")
        # Optional: Add logic to ensure date is not in the future, etc.
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
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True) # Made nullable for doctors not yet assigned

    # Relationships
    department = db.relationship('Department', back_populates='doctors')
    appointments = db.relationship('Appointment', back_populates='doctor', cascade='all, delete-orphan')
    medical_records = db.relationship('Medical_Record', back_populates='doctor', cascade='all, delete-orphan')

    # Serialization rules to prevent circular references
    serialize_rules = (
        '-appointments.doctor',
        '-medical_records.doctor',
        '-department.doctors' # Prevent endless loop if Department also serializes its doctors
    )

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
        if contact is not None and not isinstance(contact, str):
            raise ValueError("Contact must be a string or None.")
        if contact and len(contact.strip()) < 5: # Basic length check
             raise ValueError("Contact information appears too short or invalid.")
        return contact.strip() if contact else None

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
    headdoctor = db.relationship('Doctor', foreign_keys=[headdoctor_id], post_update=True) # post_update to handle potential circular dependency on updates

    serialize_rules = (
        '-doctors.department',      # Prevent circular reference: doctors should not serialize their department back
        '-headdoctor.department'    # Prevent circular reference for the head doctor relationship
    )

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

    @validates('date')
    def validate_date(self, key, date):
        if not isinstance(date, datetime):
            raise ValueError("Appointment date must be a valid datetime object.")
        # Example: Ensure appointment is not in the past
        # if date < datetime.now():
        #     raise ValueError("Appointment date cannot be in the past.")
        return date

    @validates('reason')
    def validate_reason(self, key, reason):
        if not reason or not isinstance(reason, str) or len(reason.strip()) < 5:
            raise ValueError("Reason must be a descriptive string of at least 5 characters.")
        return reason.strip()

    def __repr__(self):
        return f"<Appointment {self.id} on {self.date.strftime('%Y-%m-%d %H:%M')} for Patient {self.patient_id} with Doctor {self.doctor_id}>"


class Medical_Record(db.Model, SerializerMixin):
    __tablename__ = 'medical_records'

    id = db.Column(db.Integer, primary_key=True)
    diagnosis = db.Column(db.String(255), nullable=False) # Added length
    treatment = db.Column(db.String(255), nullable=False) # Added length
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
    def validate_date(self, key, date):
        if not isinstance(date, datetime):
            raise ValueError("Medical record date must be a valid datetime object.")
        return date

    def __repr__(self):
        return f"<Medical Record {self.id} for Patient {self.patient_id} by Doctor {self.doctor_id} on {self.date.strftime('%Y-%m-%d %H:%M')}>"