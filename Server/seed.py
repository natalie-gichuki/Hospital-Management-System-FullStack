from app import create_app, db
from app.models import Doctor, Department, Patient, Appointment, MedicalRecord, User # Import User
from datetime import date, datetime, timedelta
from sqlalchemy.exc import IntegrityError

app = create_app()

with app.app_context():
    print("Clearing existing data...")
    db.drop_all()
    db.create_all()
    print("Database cleared and recreated.")

    # --- Create Users first ---
    user_admin = User(username="admin", role="admin")
    user_admin.password = "adminpass" # Set password
    db.session.add(user_admin)
    db.session.flush() # To get user_admin.id

    user_dept_manager = User(username="dept_manager", role="department_manager")
    user_dept_manager.password = "deptpass"
    db.session.add(user_dept_manager)
    db.session.flush()

    user_doctor1 = User(username="dr_alice", role="doctor")
    user_doctor1.password = "alicesspass"
    db.session.add(user_doctor1)
    db.session.flush()

    user_doctor2 = User(username="dr_brian", role="doctor")
    user_doctor2.password = "brianspass"
    db.session.add(user_doctor2)
    db.session.flush()

    user_patient1 = User(username="jane_doe", role="patient")
    user_patient1.password = "janesspass"
    db.session.add(user_patient1)
    db.session.flush()

    user_patient2 = User(username="john_smith", role="patient")
    user_patient2.password = "johnsspass"
    db.session.add(user_patient2)
    db.session.flush()

    # --- Create Doctors and link to Users ---
    doc1 = Doctor(name="Dr. Alice Mumo", specialization="Cardiology", department_id=0, user=user_doctor1)
    db.session.add(doc1)
    db.session.flush()

    doc2 = Doctor(name="Dr. Brian Njoroge", specialization="Neurology", department_id=0, user=user_doctor2)
    db.session.add(doc2)
    db.session.flush()

    # --- Create Departments and link to Doctors as head ---
    dept1 = Department(name="Cardiology", specialty="Heart", head_doctor_id=doc1.id)
    db.session.add(dept1)
    db.session.flush()

    dept2 = Department(name="Neurology", specialty="Brain & Nervous System", head_doctor_id=doc2.id)
    db.session.add(dept2)
    db.session.flush()

    # --- Update Doctors with real department_id ---
    doc1.department_id = dept1.id
    doc2.department_id = dept2.id

    # --- Create Patients and link to Users ---
    patient1 = Patient(name="Jane Doe", date_of_birth=date(1990, 4, 12), contact_number="0712345678", user=user_patient1)
    db.session.add(patient1)
    db.session.flush()

    patient2 = Patient(name="John Smith", date_of_birth=date(1985, 7, 20), contact_number="0723456789", user=user_patient2)
    db.session.add(patient2)
    db.session.flush()

    # --- Create Appointments ---
    # Appointment for Jane Doe with Dr. Alice (Cardiology)
    appt1_date = datetime.utcnow() + timedelta(days=5, hours=10)
    appt1 = Appointment(patient=patient1, doctor=doc1, appointment_date=appt1_date, status='Scheduled')
    db.session.add(appt1)

    # Appointment for John Smith with Dr. Brian (Neurology)
    appt2_date = datetime.utcnow() + timedelta(days=2, hours=14)
    appt2 = Appointment(patient=patient2, doctor=doc2, appointment_date=appt2_date, status='Scheduled')
    db.session.add(appt2)

    # Completed appointment for Jane Doe with Dr. Alice
    appt3_date = datetime.utcnow() - timedelta(days=10, hours=9)
    appt3 = Appointment(patient=patient1, doctor=doc1, appointment_date=appt3_date, status='Completed')
    db.session.add(appt3)

    # --- Create Medical Records ---
    mr1 = MedicalRecord(
        patient=patient1,
        doctor=doc1,
        visit_date=appt3_date, # Link to the completed appointment date
        diagnosis="Common cold, mild symptoms.",
        treatment="Rest and fluids, paracetamol."
    )
    db.session.add(mr1)

    mr2 = MedicalRecord(
        patient=patient2,
        doctor=doc2,
        visit_date=datetime.utcnow() - timedelta(days=1),
        diagnosis="Migraine episode, chronic.",
        treatment="Prescribed sumatriptan and lifestyle changes."
    )
    db.session.add(mr2)


    try:
        db.session.commit()
        print("Seeding successful!")
        print("\n--- Test User Credentials ---")
        print("Admin: username='admin', password='adminpass'")
        print("Department Manager: username='dept_manager', password='deptpass'")
        print("Doctor (Alice): username='dr_alice', password='alicesspass'")
        print("Doctor (Brian): username='dr_brian', password='brianspass'")
        print("Patient (Jane): username='jane_doe', password='janesspass'")
        print("Patient (John): username='john_smith', password='johnsspass'")

    except IntegrityError as e:
        db.session.rollback()
        print("Integrity error during seeding:", e)
    except Exception as e:
        db.session.rollback()
        print("An error occurred during seeding:", e)