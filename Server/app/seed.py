
#from .models import Doctor, Patient, Department, Appointment, Medical_Record
from app import db, create_app

from faker import Faker
from datetime import datetime, timedelta
import random
from random import choice as rc

from app.models import Patient, Inpatient, Outpatient, Medical_Record, Doctor  # Ensure these are correctly imported
import random

fake = Faker()
app = create_app()

def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        print('Start Seeding...')

        # Seed Doctors
                # Seed Doctors (manual)
        print("👨‍⚕️ Seeding Doctors...")
        doctors = [
            Doctor(name="Dr. Alice Kamau", specialization="Cardiologist", contact="alice.kamau@hospital.com"),
            Doctor(name="Dr. Brian Otieno", specialization="Neurologist", contact="brian.otieno@hospital.com"),
            Doctor(name="Dr. Cynthia Mwangi", specialization="Pediatrician", contact="cynthia.mwangi@hospital.com"),
            Doctor(name="Dr. Daniel Kiprotich", specialization="Dermatologist", contact="daniel.kiprotich@hospital.com"),
            Doctor(name="Dr. Emily Wambui", specialization="General Surgeon", contact="emily.wambui@hospital.com"),
            Doctor(name="Dr. Felix Njoroge", specialization="Radiologist", contact="felix.njoroge@hospital.com"),
            Doctor(name="Dr. Grace Achieng", specialization="Gynecologist", contact="grace.achieng@hospital.com"),
            Doctor(name="Dr. Henry Kimani", specialization="Oncologist", contact="henry.kimani@hospital.com"),
            Doctor(name="Dr. Irene Mutua", specialization="ENT Specialist", contact="irene.mutua@hospital.com"),
            Doctor(name="Dr. James Mwenda", specialization="Orthopedic Surgeon", contact="james.mwenda@hospital.com"),
        ]

        for doctor in doctors:
            db.session.add(doctor)
        db.session.commit()
        print("✅ 10 Manual Doctors added.")


        # Seed Patients
        print('Seeding Patients...')
        for p in range(20):
            if random.choice(['in', 'out']) == 'in':
                patient = Inpatient(
                    name=fake.name(),
                    age=random.randint(1, 200),
                    gender=random.choice(['Male', 'Female']),
                    admission_date=str(fake.date_this_year()),
                    ward_number=random.randint(100, 999),
                    type='inpatient'
                )
            else:
                patient = Outpatient(
                    name=fake.name(),
                    age=random.randint(1, 90),
                    gender=random.choice(['Male', 'Female']),
                    last_visit_date=str(fake.date_this_year()),
                    type='outpatient'
                )
            db.session.add(patient)

        db.session.commit()

        # Seed Medical Records
        print('📋 Seeding Medical Records ...')
        patients = Patient.query.all()
        if not patients or not doctors:
            print("⚠️ Cannot seed medical records — missing patients or doctors.")
            return

        records = [
            Medical_Record(diagnosis="Flu", treatment="Rest and paracetamol", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-01-01"),
            Medical_Record(diagnosis="Asthma", treatment="Use inhaler daily", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-01-03"),
            Medical_Record(diagnosis="Malaria", treatment="Artemether-lumefantrine", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-01-05"),
            Medical_Record(diagnosis="Hypertension", treatment="Amlodipine 5mg daily", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-01-07"),
            Medical_Record(diagnosis="Diabetes", treatment="Insulin therapy", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-01-09"),
            Medical_Record(diagnosis="Migraine", treatment="Ibuprofen as needed", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-01-11"),
            Medical_Record(diagnosis="COVID-19", treatment="Home isolation + vitamins", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-01-13"),
            Medical_Record(diagnosis="Allergy", treatment="Cetirizine 10mg daily", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-01-15"),
            Medical_Record(diagnosis="Fracture", treatment="Apply cast for 6 weeks", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-01-17"),
            Medical_Record(diagnosis="Ulcer", treatment="Omeprazole 20mg daily", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-01-19"),
            Medical_Record(diagnosis="Sinusitis", treatment="Nasal spray & rest", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-01-21"),
            Medical_Record(diagnosis="Back pain", treatment="Physical therapy", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-01-23"),
            Medical_Record(diagnosis="Toothache", treatment="Tooth extraction", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-01-25"),
            Medical_Record(diagnosis="Ear infection", treatment="Antibiotic ear drops", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-01-27"),
            Medical_Record(diagnosis="Pneumonia", treatment="Azithromycin 5 days", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-01-29"),
            Medical_Record(diagnosis="Sprain", treatment="R.I.C.E therapy", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-01-31"),
            Medical_Record(diagnosis="Bronchitis", treatment="Steam & cough syrup", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-02-02"),
            Medical_Record(diagnosis="Anemia", treatment="Iron supplements", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-02-04"),
            Medical_Record(diagnosis="Chickenpox", treatment="Calamine & antihistamine", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-02-06"),
            Medical_Record(diagnosis="Thyroid disorder", treatment="Levothyroxine", patient_id=rc(patients).id, doctor_id=rc(doctors).id, date="2025-02-08"),
        ]

        for record in records:
            db.session.add(record)

        db.session.commit()
        print("✅ 20 Manual Medical Records added.")

        print("✅ Seeding complete.")

if __name__ == "__main__":
    seed_data()

