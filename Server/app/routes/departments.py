# src/api.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import date, datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from functools import wraps

# Import your database session helper and models
from app.config import get_db # Assuming get_db is your session generator
from app.models import Department, Doctor, Patient, InPatient, OutPatient, Appointment, MedicalRecord, PatientType, AppointmentStatus

app = Flask(__name__)
CORS(app) # Enable CORS for all routes, allowing your React frontend to access it

# --- Decorator for database session management ---
def with_db_session(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session = next(get_db())
        try:
            # Pass session as the first argument to the route function
            result = f(session, *args, **kwargs)
            return result
        except SQLAlchemyError as e:
            session.rollback()
            app.logger.error(f"Database error: {e}")
            return jsonify({"error": "Database error occurred"}), 500
        except Exception as e:
            app.logger.error(f"An unexpected error occurred: {e}")
            return jsonify({"error": str(e)}), 500
        finally:
            session.close()
    return decorated_function

# --- API Endpoints for Department Management ---

@app.route('/departments', methods=['GET'])
@with_db_session
def get_departments(session):
    departments = Department.get_all(session)
    return jsonify([dept.to_dict() for dept in departments])

@app.route('/departments/<int:department_id>', methods=['GET'])
@with_db_session
def get_department(session, department_id):
    dept = Department.get_by_id(session, department_id)
    if not dept:
        return jsonify({"error": "Department not found"}), 404
    return jsonify(dept.to_dict())

@app.route('/departments', methods=['POST'])
@with_db_session
def add_department(session):
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"error": "Department name is required"}), 400
    
    head_doctor_id = data.get('head_doctor_id')
    if head_doctor_id and not Doctor.get_by_id(session, head_doctor_id):
        return jsonify({"error": f"Doctor with ID {head_doctor_id} not found."}), 400

    try:
        dept = Department(
            name=name,
            specialty=data.get('specialty'),
            head_doctor_id=head_doctor_id
        )
        dept.save(session)
        return jsonify(dept.to_dict()), 201
    except IntegrityError: # More specific than ValueError for unique constraints
        return jsonify({"error": f"Department with name '{name}' already exists."}), 409

@app.route('/departments/<int:department_id>', methods=['PUT'])
@with_db_session
def update_department_api(session, department_id):
    data = request.get_json()
    dept = Department.get_by_id(session, department_id)
    if not dept:
        return jsonify({"error": "Department not found"}), 404

    try:
        dept.name = data.get('name', dept.name)
        dept.specialty = data.get('specialty', dept.specialty)
        
        if 'head_doctor_id' in data:
            head_id = data['head_doctor_id']
            if head_id is not None and not Doctor.get_by_id(session, head_id):
                return jsonify({"error": f"Doctor with ID {head_id} not found."}), 400
            dept.head_doctor_id = head_id
        
        dept.save(session)
        return jsonify(dept.to_dict()), 200
    except IntegrityError:
        return jsonify({"error": "Update failed, likely due to a duplicate name."}), 409

@app.route('/departments/<int:department_id>', methods=['DELETE'])
@with_db_session
def delete_department_api(session, department_id):
    dept = Department.get_by_id(session, department_id)
    if not dept:
        return jsonify({"error": "Department not found"}), 404
    
    dept.delete(session)
    return jsonify({"message": "Department deleted successfully"}), 200
