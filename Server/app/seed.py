from app.models import Doctor, Patient, Inpatient, Outpatient, MedicalRecord
from app import db, create_app
from faker import Faker
import random
from random import choice as rc

fake = Faker()
app = create_app()

def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        print("🔁 Dropped and recreated all tables.")
        print("🌱 Starting seeding...")

        # === Doctors ===
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
        db.session.add_all(doctors)
        db.session.commit()
        print("✅ 10 Doctors added.")

        # === Patients (in/out/base) ===
        print("🧑‍⚕️ Seeding Patients...")
        for _ in range(20):
            kind = random.choice(['inpatient', 'outpatient', 'base'])
            if kind == 'inpatient':
                patient = Inpatient(
                    name=fake.name(),
                    age=random.randint(1, 100),
                    gender=random.choice(['Male', 'Female']),
                    admission_date=str(fake.date_this_year()),
                    ward_number=random.randint(100, 999)
                )
            elif kind == 'outpatient':
                patient = Outpatient(
                    name=fake.name(),
                    age=random.randint(1, 100),
                    gender=random.choice(['Male', 'Female']),
                    last_visit_date=str(fake.date_this_year())
                )
            else:
                patient = Patient(
                    name=fake.name(),
                    age=random.randint(1, 100),
                    gender=random.choice(['Male', 'Female'])
                )
            db.session.add(patient)

        db.session.commit()
        print("✅ 20 Mixed Patients (in/out/base) added.")

        # === Medical Records ===
        print("📋 Seeding Medical Records...")
        patients = Patient.query.all()
        if not patients or not doctors:
            print("⚠️ Cannot seed medical records — missing patients or doctors.")
            return

        conditions = [
            ("Flu", "Rest and paracetamol"),
            ("Asthma", "Use inhaler daily"),
            ("Malaria", "Artemether-lumefantrine"),
            ("Hypertension", "Amlodipine 5mg daily"),
            ("Diabetes", "Insulin therapy"),
            ("Migraine", "Ibuprofen as needed"),
            ("COVID-19", "Home isolation + vitamins"),
            ("Allergy", "Cetirizine 10mg daily"),
            ("Fracture", "Apply cast for 6 weeks"),
            ("Ulcer", "Omeprazole 20mg daily"),
            ("Sinusitis", "Nasal spray & rest"),
            ("Back pain", "Physical therapy"),
            ("Toothache", "Tooth extraction"),
            ("Ear infection", "Antibiotic ear drops"),
            ("Pneumonia", "Azithromycin 5 days"),
            ("Sprain", "R.I.C.E therapy"),
            ("Bronchitis", "Steam & cough syrup"),
            ("Anemia", "Iron supplements"),
            ("Chickenpox", "Calamine & antihistamine"),
            ("Thyroid disorder", "Levothyroxine"),
        ]

        for i, (diagnosis, treatment) in enumerate(conditions):
            record = MedicalRecord(
                diagnosis=diagnosis,
                treatment=treatment,
                patient_id=rc(patients).id,
                doctor_id=rc(doctors).id,
                visit_date=datetime(2025, 1, 1) + timedelta(days=i * 2)
            )
            db.session.add(record)

        db.session.commit()
        print("✅ 20 Medical Records added.")

        print("🎉 Seeding complete.")

if __name__ == "__main__":
    seed_data()
