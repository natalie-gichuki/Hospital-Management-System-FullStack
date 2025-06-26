from app import create_app, db
from app.models import Doctor, Department, Patient
from sqlalchemy.exc import IntegrityError

app = create_app()

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Step 1: Create Doctor (without department_id for now)
    doc1 = Doctor(name="Dr. Alice Mumo", specialization="Cardiology", department_id=0)  # temp id
    db.session.add(doc1)
    db.session.flush()  # Gets the doc1.id

    # Step 2: Create Department with that doctor as head
    dept1 = Department(name="Cardiology", specialty="Heart", head_doctor_id=doc1.id)
    db.session.add(dept1)
    db.session.flush()  # Gets the dept1.id

    # Step 3: Update doctor with real department_id
    doc1.department_id = dept1.id

    # Additional examples:
    doc2 = Doctor(name="Dr. Brian", specialization="Neurology", department_id=dept1.id)
    db.session.add(doc2)

    patient1 = Patient(name="Jane Doe", date_of_birth="1990-04-12", contact_number="0712345678")
    db.session.add(patient1)

    try:
        db.session.commit()
        print("Seeding successful!")
    except IntegrityError as e:
        db.session.rollback()
        print("Integrity error during seeding:", e)
