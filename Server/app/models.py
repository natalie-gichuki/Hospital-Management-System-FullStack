# Have the models here (PATIENTS, DOCTORS, DEPARTMENTS, APPOINTMENTS, MEDICAL_RECORDS)
from app import db
from datetime import datetime, date
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError

class Doctor(db.Model, SerializerMixin):
    __tablename__ = 'doctors'

    # Serialization rules to prevent infinite recursion with related models.
    serialize_rules = (
        '-department.doctors_in_department', 
        '-department.head_doctor', 
        '-departments_headed', 
        '-appointments.doctor',
        '-medical_records.doctor'
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)

    # Relationships
    # The department this doctor belongs to.
    department = db.relationship('Department', back_populates='doctors_in_department', foreign_keys=[department_id])
    # The departments this doctor is the head of.
    departments_headed = db.relationship('Department', back_populates='head_doctor', foreign_keys='Department.head_doctor_id')
    # Appointments scheduled with this doctor.
    appointments = db.relationship('Appointment', back_populates='doctor', cascade="all, delete-orphan")
    # Medical records created by this doctor.
    medical_records = db.relationship('Medical_record', back_populates='doctor', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Doctor(id={self.id}, name='{self.name}', specialization='{self.specialization}')>"

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

class Patient(db.Model, SerializerMixin):
    __tablename__ = 'patients'
    serialize_rules = ('-appointments.patient', '-medical_records.patient')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    contact_number = db.Column(db.String(20), nullable=False, unique=True)

    # Relationships
    appointments = db.relationship('Appointment', back_populates='patient', cascade="all, delete-orphan")
    medical_records = db.relationship('Medical_record', back_populates='patient', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Patient(id={self.id}, name='{self.name}')>"

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 2:
            raise ValueError("Patient name must be at least 2 characters long.")
        return name
    
    @validates('contact_number')
    def validate_contact_number(self, key, contact_number):
        # A simple validation. This could be improved with a regex for more specific formats.
        if not contact_number or not contact_number.replace('+', '').isdigit() or len(contact_number) < 10:
            raise ValueError("Contact number must be a valid phone number with at least 10 digits.")
        return contact_number

class Department(db.Model, SerializerMixin):
    __tablename__ = 'departments'
    serialize_rules = ('-doctors_in_department.department', '-head_doctor.departments_headed', '-head_doctor.department')
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    specialty = db.Column(db.String(100), nullable=False)
    head_doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)

    # Relatiionships
    #Doctors in the department
    doctors_in_department = db.relationship(
        'Doctor',
        back_populates='department',
        foreign_keys='Doctor.department_id'
    )
    # head doctor of the department
    head_doctor = db.relationship(
        'Doctor', 
        back_populates='departments_headed',
        foreign_keys=[head_doctor_id], # Use the column object here
        uselist=False,
        post_update=True
    )
    # Patients assigned to the department
    # patients_assigned = db.relationship("Patient", back_populates='assigned_department', foreign_keys=[Patient.assigned_department_id])

    def __repr__(self):
        head_name = self.head_doctor.name if self.head_doctor else "No Head Doctor"
        return f"<Department(id: {self.id}, name: {self.name}, specialty={self.specialty}, head='{head_name}')>"
    
    #CRUD METHODS FOR DEPARTMENT CLASS
    def save(self):
        db.session.add(self) 
        try:
            db.session.commit()
            return self
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Department with this name already exists")
    # To delete a department from the database
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def get_by_id(cls, session, id):
        department = session.query(cls).filter_by(id=id).first()
        if not department:
            raise ValueError(f"Department with the id: {id} does not exist")
        return department
    
    @classmethod
    def get_all(cls, session): 
        departments = session.query(cls).all()
        if not departments:
            raise ValueError("No departments found")
        return departments
    
    @classmethod
    def get_by_name(cls, session, name):
        department = session.query(cls).filter_by(name=name).first()
        if not department:
            raise ValueError(f"Department with the name: {name} does not exist")
        return department
    
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Department name cannot be empty")
        if len(name) < 3:
            raise ValueError("Department name must be at least 3 characters long")
        return name
    
    @validates('specialty')
    def validate_specialty(self, key, specialty):
        if not specialty:
            raise ValueError("Department specialty cannot be empty")
        if len(specialty) < 3:
            raise ValueError("Department specialty must be at least 3 characters long")
        return specialty
    
    @validates('head_doctor_id')
    def validate_head_doctor_id(self, key, head_doctor_id):
        if head_doctor_id is None:
            raise ValueError("Head doctor ID cannot be empty")
        if not isinstance(head_doctor_id, int):
            raise ValueError("Head doctor ID must be an integer")
        return head_doctor_id
    
    def save(self, session):
        """Adds or updates a department in the database."""
        session.add(self)
        try:
            session.commit()
            return self
        except IntegrityError:
            session.rollback()
            raise ValueError("Department with this name already exists.")

    def delete(self, session):
        """Deletes a department from the database."""
        session.delete(self)
        session.commit()

    @classmethod
    def get_by_id(cls, session, department_id):
        """Retrieves a department by ID."""
        return session.query(cls).filter_by(id=department_id).first()

    @classmethod
    def get_all(cls, session):
        """Retrieves all departments."""
        return session.query(cls).all()

    def to_dict(self):
        """Serializes a Department object to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "specialty": self.specialty,
            "head_doctor_id": self.head_doctor_id,
            "head_doctor_name": self.head_doctor.name if self.head_doctor else None,
            "num_doctors_in_dept": len(self.doctors_in_department),
            "num_patients_assigned": len(self.patients_assigned)
        }

class Appointment(db.Model, SerializerMixin):
    __tablename__ = 'appointments'
    serialize_rules = ('-patient.appointments', '-doctor.appointments')

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Scheduled') # e.g., Scheduled, Completed, Canceled

    # Relationships
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

class Medical_record(db.Model, SerializerMixin):
    __tablename__ = 'medical_records'
    serialize_rules = ('-patient.medical_records', '-doctor.medical_records')

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    visit_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    diagnosis = db.Column(db.Text, nullable=False)
    treatment = db.Column(db.Text, nullable=False)

    # Relationships
    patient = db.relationship('Patient', back_populates='medical_records')
    doctor = db.relationship('Doctor', back_populates='medical_records')

    @validates('diagnosis', 'treatment')
    def validate_text_fields(self, key, value):
        if not value or len(value) < 5:
            raise ValueError(f"{key.capitalize()} must be at least 5 characters long.")
        return value

    

    
