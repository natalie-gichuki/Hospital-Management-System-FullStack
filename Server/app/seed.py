from .models import Doctor, Appointment, Patient
from . import db, create_app
from faker import Faker
from datetime import datetime, timedelta
import random
from random import choice as rc

app = create_app()

with app.app_context():
    print("Seeding data...")

    # Clear existing data
    Appointment.query.delete()
    Doctor.query.delete()
    Patient.query.delete()

    # Create doctors
    doctor1 = Doctor(name="Dr. Alice Smith", specialization="Cardiology")
    doctor2 = Doctor(name="Dr. Bob Johnson", specialization="Neurology")

    # Create patients
    patient1 = Patient(name="John Doe", gender="Male", admission_type="Inpatient")
    patient2 = Patient(name="Jane Doe", gender="Female", admission_type="Outpatient")

    db.session.add_all([doctor1, doctor2, patient1, patient2])
    db.session.commit()

    # Create appointments
    appointment1 = Appointment(
        date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        reason="Routine checkup",
        patient_id=patient1.id,
        doctor_id=doctor1.id
    )

    appointment2 = Appointment(
        date=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
        reason="Follow-up visit",
        patient_id=patient2.id,
        doctor_id=doctor2.id
    )

    db.session.add_all([appointment1, appointment2])
    db.session.commit()

    print("✅ Seeded doctors, patients, and appointments.")