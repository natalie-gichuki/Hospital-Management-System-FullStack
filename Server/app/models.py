# Have the models here (PATIENTS, DOCTORS, DEPARTMENTS, APPOINTMENTS, MEDICAL_RECORDS)
from app import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError

class Department(db.Model, SerializerMixin):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    specialty = db.Column(db.String(100), nullable=False)
    head_doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)

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



    

    
