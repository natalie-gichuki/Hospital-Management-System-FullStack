from app import db, create_app
from app.models import User, Doctor, Department, Patient, Inpatient, Outpatient, Appointment, MedicalRecord
from faker import Faker
from datetime import datetime, timedelta
import random
from random import choice as rc

fake = Faker()
app = create_app()

def seed_data():
    with app.app_context():
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        print("Database cleared and recreated.")

        # === USERS, DOCTORS & DEPARTMENTS ===
        print("Seeding Departments, Doctors & Users...")
        departments_data = [
            ("Cardiology", "Heart specialist"),
            ("Neurology", "Brain specialist"),
            ("Pediatrics", "Child specialist"),
            ("Dermatology", "Skin specialist"),
            ("Surgery", "General surgery"),
        ]

        doctors = []
        departments = []
        for name, specialty in departments_data:
            doc_name = fake.name()
            user = User(username=doc_name.lower().replace(" ", ""), password="password", role="doctor")
            doctor = Doctor(
                name=doc_name,
                specialization=specialty,
                contact=fake.email(),
                user=user
            )
            dept = Department(name=name, specialty=specialty, head_doctor=doctor)
            doctor.department = dept

            db.session.add(user)
            db.session.add(doctor)
            db.session.add(dept)

            doctors.append(doctor)
            departments.append(dept)

        db.session.commit()
        print(f"✅ {len(doctors)} Doctors, Users, and Departments created.")

        # === PATIENTS & USERS ===
        print("Seeding Patients & Users...")
        patients = []
        for _ in range(20):
            name = fake.name()
            role = rc(["inpatient", "outpatient", "patient"])
            user = User(username=name.lower().replace(" ", ""), password="password", role="patient")

            if role == "inpatient":
                patient = Inpatient(
                    name=name,
                    age=random.randint(1, 90),
                    gender=rc(["Male", "Female"]),
                    admission_date=str(fake.date_this_year()),
                    ward_number=random.randint(100, 300),
                    user=user
                )
            elif role == "outpatient":
                patient = Outpatient(
                    name=name,
                    age=random.randint(1, 90),
                    gender=rc(["Male", "Female"]),
                    last_visit_date=str(fake.date_this_year()),
                    user=user
                )
            else:
                patient = Patient(
                    name=name,
                    age=random.randint(1, 90),
                    gender=rc(["Male", "Female"]),
                    user=user
                )

            db.session.add(user)
            db.session.add(patient)
            patients.append(patient)

        db.session.commit()
        print(f"✅ {len(patients)} Patients & Users added.")

        # === APPOINTMENTS ===
        print("Seeding Appointments...")
        reasons = [
            "Routine checkup", "Follow-up visit", "New symptoms", "Lab results review",
            "Skin rash evaluation", "Chronic pain management", "Vaccination", "Blood pressure monitoring"
        ]

        for _ in range(15):
            appt = Appointment(
                appointment_date=datetime.utcnow() + timedelta(days=random.randint(-10, 10), hours=random.randint(8, 17)),
                reason=rc(reasons),
                status=rc(["Scheduled", "Completed", "Cancelled"]),
                patient=rc(patients),
                doctor=rc(doctors)
            )
            db.session.add(appt)

        db.session.commit()
        print("✅ 15 Appointments created.")

        # === MEDICAL RECORDS ===
        print("Seeding Medical Records...")
        for _ in range(20):
            record = MedicalRecord(
                diagnosis=fake.word().capitalize(),
                treatment=fake.sentence(nb_words=4),
                visit_date=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                patient=rc(patients),
                doctor=rc(doctors)
            )
            db.session.add(record)

        db.session.commit()
        print("✅ 20 Medical Records created.")
        print("🎉 Seeding complete!")

if __name__ == "__main__":
    seed_data()
