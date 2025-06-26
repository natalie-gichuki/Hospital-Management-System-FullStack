# src/api.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import date, datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# Import your database session helper and models
from app.config import get_db # Assuming get_db is your session generator
from app.models import Department, Doctor, Patient, InPatient, OutPatient, Appointment, MedicalRecord, PatientType, AppointmentStatus

app = Flask(__name__)
CORS(app) # Enable CORS for all routes, allowing your React frontend to access it

# --- API Endpoints for Department Management ---

@app.route('/departments', methods=['GET'])
def get_departments():
    session = next(get_db())9
    try:
        departments = Department.get_all(session)
        return jsonify([dept.to_dict() for dept in departments])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/departments/<int:department_id>', methods=['GET'])
def get_department(department_id):
    session = next(get_db())
    try:
        dept = Department.get_by_id(session, department_id)
        if not dept:
            return jsonify({"error": "Department not found"}), 404
        return jsonify(dept.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@app.route('/departments', methods=['POST'])
def add_department():
    session = next(get_db())
    data = request.get_json()
    name = data.get('name')
    specialty = data.get('specialty')
    head_doctor_id = data.get('head_doctor_id')

    if not name:
        return jsonify({"error": "Department name is required"}), 400

    try:
        # Validate head_doctor_id if provided
        if head_doctor_id:
            doctor = Doctor.get_by_id(session, head_doctor_id)
            if not doctor:
                return jsonify({"error": f"Doctor with ID {head_doctor_id} not found."}), 400

        dept = Department(name=name, specialty=specialty, head_doctor_id=head_doctor_id)
        dept.save(session)
        return jsonify(dept.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409 # Conflict, e.g., unique name violation
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": "Database error occurred"}), 500
    finally:
        session.close()

@app.route('/departments/<int:department_id>', methods=['PUT'])
def update_department_api(department_id):
    session = next(get_db())
    data = request.get_json()

    try:
        dept = Department.get_by_id(session, department_id)
        if not dept:
            return jsonify({"error": "Department not found"}), 404

        if 'name' in data:
            dept.name = data['name']
        if 'specialty' in data:
            dept.specialty = data['specialty']
        if 'head_doctor_id' in data:
            head_doctor_id = data['head_doctor_id']
            if head_doctor_id is not None:
                doctor = Doctor.get_by_id(session, head_doctor_id)
                if not doctor:
                    return jsonify({"error": f"Doctor with ID {head_doctor_id} not found."}), 400
            dept.head_doctor_id = head_doctor_id # Can be None

        dept.save(session)
        return jsonify(dept.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": "Database error occurred"}), 500
    finally:
        session.close()

@app.route('/departments/<int:department_id>', methods=['DELETE'])
def delete_department_api(department_id):
    session = next(get_db())
    try:
        dept = Department.get_by_id(session, department_id)
        if not dept:
            return jsonify({"error": "Department not found"}), 404
        
        dept.delete(session)
        return jsonify({"message": "Department deleted successfully"}), 200
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({"error": "Database error occurred"}), 500
    finally:
        session.close()
