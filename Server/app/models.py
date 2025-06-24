# Have the models here (PATIENTS, DOCTORS, DEPARTMENTS, APPOINTMENTS, MEDICAL_RECORDS)
from app import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

class Department(db.model, SerializerMixin):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, db.ForeignKey('patients.assigned_department_id', primary_key=True), nullable=False)
    name = db.column(db.string(100), nullable=False, unique=True)
    specialty = db.column(db.string(100), nullable=False)
    head_doctor_id = db.column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)

    # Relatiionships
    #Doctors in the department
    doctors_in_department = db.relationship(
        'Doctor',
        back_populates='departments',
        foreign_keys='Doctor.department_id'
    )
    # head doctor of the department
    head_doctor = db.relationship(
        'Doctor', 
        back_populates='departments_headed',
        foreign_keys=[head_doctor_id],
        uselist=False,
        post_update=True
    )
    # Patients assigned to the department
    patients_assigned = db.relationship("Patient", back_populates='assigned_department', foreign_keys=[Patient.assigned_department_id])

    def __repr__(self):
        head_name = self.head_doctor.name if self.head_doctor else "No Head Doctor"
        return f"<Department(id: {self.id}, name: {self.name}, specialty={self.specialty}, head='{head_name}')>"
    
    

    
