from app import db, create_app
# Ensure these imports match your actual model names (e.g., Medical_Record vs MedicalRecord)
from app.models import User, Doctor, Department, Patient, Inpatient, Outpatient, Appointment, Medical_Record
from faker import Faker
from datetime import datetime, timedelta, date # Import date for db.Date columns
import random
from random import choice as rc

fake = Faker()
app = create_app()

def seed_data():
    with app.app_context():
        print("Clearing existing data...")
        # Order matters for dropping tables due to foreign key constraints
        # It's usually safer to drop all then recreate all.
        db.drop_all()
        db.create_all() # Recreate tables based on current models
        print("Database cleared and recreated.")

        print('Start Seeding...')

        # Lists to hold created objects for later use
        doctors = []
        departments = []
        patients = []

        # === DEPARTMENTS, DOCTORS & USERS ===
        print("Seeding Departments, Doctors & Users...")

        # Define departments and their associated specialties
        departments_data = [
            ("Cardiology", "Heart specialist"),
            ("Neurology", "Brain specialist"),
            ("Pediatrics", "Child specialist"),
            ("Dermatology", "Skin specialist"),
            ("Surgery", "General surgery"),
            ("Radiology", "Diagnostic Imaging"),
            ("Gynecology", "Women's Health"),
            ("Oncology", "Cancer Treatment"),
            ("ENT", "Ear, Nose, Throat"),
            ("Orthopedics", "Bone and Joint")
        ]

        # Create departments, a user for each doctor, and a doctor
        # Assign a doctor as head_doctor to their department
        for name, specialty in departments_data:
            doc_name = fake.name()
            # Create a user for the doctor
            user = User(username=doc_name.lower().replace(" ", "") + str(random.randint(1, 99)), password="password", role="doctor")
            db.session.add(user) # Add user first to get an ID

            # Create the doctor, linking to the user
            doctor = Doctor(
                name=doc_name,
                specialization=specialty,
                contact=fake.email(),
                user=user # Link the User object
            )
            db.session.add(doctor) # Add doctor to session to get an ID for department linkage

            # Create the department, linking the doctor as head doctor and also as a general doctor
            dept = Department(
                name=name,
                specialty=specialty,
                headdoctor=doctor # Link the Doctor object as head doctor
            )
            db.session.add(dept) # Add department to session

            # Establish the bidirectional link: doctor's department
            doctor.department = dept

            departments.append(dept)
            doctors.append(doctor)

        db.session.commit()
        print(f"✅ {len(departments)} Departments and {len(doctors)} Doctors (with Users) created.")

        # === PATIENTS & USERS ===
        print("Seeding Patients & Users...")
        patient_types = ["inpatient", "outpatient"] # Using these specifically, 'patient' type is general parent

        for _ in range(30): # Increased patient count for more variety
            name = fake.name()
            # Ensure unique username
            username = name.lower().replace(" ", "") + str(random.randint(100, 999))
            # Create a user for the patient
            user = User(username=username, password="password", role="patient")
            db.session.add(user)

            patient_type_choice = rc(patient_types)
            patient_obj = None

            if patient_type_choice == "inpatient":
                patient_obj = Inpatient(
                    name=name,
                    age=random.randint(1, 90),
                    gender=rc(["Male", "Female", "Other"]), # Added 'Other' for gender
                    admission_date=fake.date_this_year(before_today=True, after_today=False), # Use date object directly
                    ward_number=random.randint(100, 300),
                    user=user # Link the User object
                )
            elif patient_type_choice == "outpatient":
                patient_obj = Outpatient(
                    name=name,
                    age=random.randint(1, 90),
                    gender=rc(["Male", "Female", "Other"]), # Added 'Other' for gender
                    last_visit_date=fake.date_this_year(before_today=True, after_today=False), # Use date object directly
                    user=user # Link the User object
                )
            # Default to a generic Patient if you have a use case for it, otherwise omit
            # else:
            #     patient_obj = Patient(
            #         name=name,
            #         age=random.randint(1, 90),
            #         gender=rc(["Male", "Female", "Other"]),
            #         user=user
            #     )

            if patient_obj:
                db.session.add(patient_obj)
                patients.append(patient_obj)

        db.session.commit()
        print(f"✅ {len(patients)} Patients (Inpatients/Outpatients with Users) added.")

        # === APPOINTMENTS ===
        print("Seeding Appointments...")
        reasons = [
            "Routine checkup", "Follow-up visit", "New symptoms", "Lab results review",
            "Skin rash evaluation", "Chronic pain management", "Vaccination", "Blood pressure monitoring",
            "Post-surgery follow-up", "Consultation for specialist referral"
        ]

        if not patients or not doctors:
            print("Skipping Appointments seeding: No patients or doctors available.")
        else:
            for _ in range(40): # Increased appointment count
                # Generate a date within a reasonable range (e.g., past 30 days to next 30 days)
                appt_date = datetime.now() + timedelta(days=random.randint(-30, 30), hours=random.randint(8, 17), minutes=random.randint(0, 59))
                
                # Ensure patient and doctor lists are not empty
                if patients and doctors:
                    appt = Appointment(
                        date=appt_date, # Use 'date' as per model
                        reason=rc(reasons),
                        # Status can be dynamic
                        status=rc(["Scheduled", "Completed", "Cancelled"]),
                        patient=rc(patients),
                        doctor=rc(doctors)
                    )
                    db.session.add(appt)
                else:
                    print("Could not create appointment: Missing patient or doctor.")

            db.session.commit()
            print(f"✅ {db.session.query(Appointment).count()} Appointments created.")

        # === MEDICAL RECORDS ===
        print("Seeding Medical Records...")
        if not patients or not doctors:
            print("Skipping Medical Records seeding: No patients or doctors available.")
        else:
            for _ in range(50): # Increased medical record count
                # Generate a date in the past for medical records
                record_date = datetime.now() - timedelta(days=random.randint(1, 365), hours=random.randint(8, 17), minutes=random.randint(0, 59))
                
                if patients and doctors:
                    record = Medical_Record( # Use Medical_Record as per your models.py
                        diagnosis=fake.sentence(nb_words=6), # More descriptive diagnosis
                        treatment=fake.paragraph(nb_sentences=2), # More descriptive treatment
                        date=record_date, # Use 'date' as per model
                        patient=rc(patients),
                        doctor=rc(doctors)
                    )
                    db.session.add(record)
                else:
                    print("Could not create medical record: Missing patient or doctor.")

            db.session.commit()
            print(f"✅ {db.session.query(Medical_Record).count()} Medical Records created.")

        print("🎉 Seeding complete!")

if __name__ == "__main__":
    seed_data()