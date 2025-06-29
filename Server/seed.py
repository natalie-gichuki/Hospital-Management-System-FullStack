from app import db, create_app
from app.models import User, Doctor, Department, Patient, Inpatient, Outpatient, Appointment, Medical_Record
from faker import Faker
from datetime import datetime, timezone, timedelta
import random
from random import choice as rc

fake = Faker()
app = create_app()

def seed_data():
    with app.app_context():
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        print("✅ Database cleared and recreated.")

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

        # First, create doctors and users without department links
        for _ in range(len(departments_data)):
            doc_name = fake.name()
            user = User(
                username=doc_name.lower().replace(" ", ""),
                password="password",
                role="doctor"
            )
            doctor = Doctor(
                name=doc_name,
                specialization=fake.job(),
                contact=fake.email(),
                user=user
            )
            db.session.add_all([user, doctor])
            doctors.append(doctor)

        db.session.commit()  # ✅ Commit doctors first

        # Now create departments and assign head doctors
        for i, (dept_name, specialty) in enumerate(departments_data):
            dept = Department(
                name=dept_name,
                specialty=specialty,
                headdoctor=doctors[i]
            )
            doctors[i].department = dept
            db.session.add(dept)
            departments.append(dept)

        db.session.commit()
        print(f"✅ {len(doctors)} Doctors, Users, and Departments created.")

        # === PATIENTS & USERS ===
        print("Seeding Patients & Users...")
        patients = []
        for _ in range(20):
            name = fake.name()
            role = rc(["inpatient", "outpatient", "patient"])
            user = User(
                username=name.lower().replace(" ", ""),
                password="password",
                role="patient"
            )

            if role == "inpatient":
                patient = Inpatient(
                    name=name,
                    age=random.randint(1, 90),
                    gender=rc(["Male", "Female", "Other"]),
                    admission_date=fake.date_this_year(),
                    ward_number=random.randint(100, 300),
                    user=user
                )
            elif role == "outpatient":
                patient = Outpatient(
                    name=name,
                    age=random.randint(1, 90),
                    gender=rc(["Male", "Female", "Other"]),
                    last_visit_date=fake.date_this_year(),
                    user=user
                )
            else:
                patient = Patient(
                    name=name,
                    age=random.randint(1, 90),
                    gender=rc(["Male", "Female", "Other"]),
                    user=user
                )

            db.session.add_all([user, patient])
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
                date=datetime.utcnow() + timedelta(days=random.randint(-10, 10), hours=random.randint(8, 17)),
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
            # Ensure diagnosis has at least 5 characters
            while True:
                diagnosis = fake.sentence(nb_words=3).strip('.')
                if len(diagnosis) >= 5:
                    break

            treatment = fake.sentence(nb_words=4).strip('.')

            record = Medical_Record(
                diagnosis=diagnosis,
                treatment=treatment,
                date=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
                patient=rc(patients),
                doctor=rc(doctors)
            )
            db.session.add(record)

        db.session.commit()
        print("✅ 20 Medical Records created.")
        print("🎉 Seeding complete!")

if __name__ == "__main__":
    seed_data()
