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
    appointments = db.relationship('Appointment', back_populates='patient', cascade='all, delete-orphan')

    serialize_rules = ('-medical_records.patient',)



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
    '-doctor.department',
    '-doctor.appointments',
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
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    # Relationships
    department = db.relationship('Department', back_populates='doctors', foreign_keys=[department_id])
    appointments = db.relationship('Appointment', back_populates='doctor', cascade='all, delete-orphan')
    medical_records = db.relationship('Medical_Record', back_populates='doctor', cascade='all, delete-orphan')

    serialize_rules = (
    '-appointments.doctor',
    '-department.doctors',
    '-department.headdoctor',
    '-medical_records.doctor',
    '-medical_records.patient',
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

    serialize_rules = ('-patient.appointments', '-doctor.appointments')

    def __repr__(self):
        return f"<Appointment {self.date} with Doctor {self.doctor_id}>"

class Department(db.Model, SerializerMixin):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    headdoctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), unique=True, nullable=True)

    # Relationship to all doctors in this department
    doctors = db.relationship(
        'Doctor',
        back_populates='department',
        cascade='all, delete-orphan',
        foreign_keys='Doctor.department_id'
    )

    # Relationship to the head doctor of this department
    headdoctor = db.relationship(
        'Doctor',
        foreign_keys=[headdoctor_id],
        post_update=True  # allows the head doctor to also belong to this department
    )

    # Serialization rules to avoid circular references in JSON output
    serialize_rules = (
    '-doctors.department',
    '-doctors.medical_records',
    '-doctors.appointments',
    '-headdoctor.department',
    '-headdoctor.appointments',
    '-headdoctor.medical_records',
)


    # === Class-level utility methods ===

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def get_by_id(cls, session, id):
        return session.query(cls).get(id)

    def save(self, session):
        session.add(self)
        session.commit()

    def delete(self, session):
        session.delete(self)
        session.commit()

    # === Validators ===

    @validates('name')
    def validate_name(self, key, name):
        if not name or not isinstance(name, str) or not name.strip():
            raise ValueError("Department name must be a non-empty string.")
        return name.strip()

    @validates('specialty')
    def validate_specialty(self, key, specialty):
        if not specialty or not isinstance(specialty, str) or not specialty.strip():
            raise ValueError("Specialty must be a non-empty string.")
        return specialty.strip()

    def __repr__(self):
        return f"<Department {self.id}: {self.name} ({self.specialty})>"
