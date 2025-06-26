from flask import request, jsonify
from flask_restful import Resource
from app.models import Patient
from app import db
from app.routes.auth import role_required # Import our custom role decorator
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class PatientList(Resource):
    """Resource for listing and creating patients."""

    @role_required(['admin', 'doctor', 'department_manager']) # Admins, Doctors, Dept Managers can view patients
    def get(self):
        try:
            patients = Patient.query.all()
            patient_list = [patient.to_dict() for patient in patients]
            return jsonify(patient_list), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @role_required(['admin', 'department_manager', 'doctor']) # Admins, Dept Managers, Doctors can register patients
    def post(self):
        try:
            data = request.get_json()

            name = data.get('name')
            date_of_birth_str = data.get('date_of_birth')
            contact_number = data.get('contact_number')
            user_id = data.get('user_id') # Optional: link to a User

            if not name or not date_of_birth_str or not contact_number:
                return jsonify({'error': 'Name, date_of_birth, and contact_number are required'}), 400

            try:
                date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date_of_birth format. Use YYYY-MM-DD'}), 400

            if Patient.query.filter_by(contact_number=contact_number).first():
                return jsonify({'error': 'Patient with this contact number already exists'}), 409

            new_patient = Patient(
                name=name,
                date_of_birth=date_of_birth,
                contact_number=contact_number,
                user_id=user_id
            )

            db.session.add(new_patient)
            db.session.commit()

            return jsonify(new_patient.to_dict()), 201
        except ValueError as ve:
            db.session.rollback()
            return jsonify({'error': str(ve)}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Integrity error, e.g., duplicate contact number or user_id, or invalid foreign key'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

class PatientByID(Resource):
    """Resource for interacting with a specific patient by ID."""

    @role_required(['admin', 'doctor', 'patient', 'department_manager']) # Admins, Doctors, Patients (their own), Dept Managers can view
    def get(self, id):
        try:
            patient = Patient.query.get(id)
            if not patient:
                return jsonify({'error': 'Patient not found'}), 404

            # Ensure patients can only view their own record unless they are admin/doctor/dept_manager
            from flask_jwt_extended import get_jwt_identity, current_user
            if current_user.role == 'patient' and current_user.patient and current_user.patient.id != patient.id:
                return jsonify({"msg": "Access denied: Patients can only view their own records"}), 403

            return jsonify(patient.to_dict()), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @role_required(['admin', 'department_manager', 'doctor']) # Admins, Dept Managers, Doctors can update patient info
    def patch(self, id):
        try:
            patient = Patient.query.get(id)
            if not patient:
                return jsonify({'error': 'Patient not found'}), 404

            data = request.get_json()

            if 'name' in data:
                patient.name = data['name']
            if 'date_of_birth' in data:
                try:
                    patient.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({'error': 'Invalid date_of_birth format. Use YYYY-MM-DD'}), 400
            if 'contact_number' in data:
                if Patient.query.filter_by(contact_number=data['contact_number']).first() and data['contact_number'] != patient.contact_number:
                    return jsonify({'error': 'Patient with this contact number already exists'}), 409
                patient.contact_number = data['contact_number']
            if 'user_id' in data:
                patient.user_id = data['user_id'] # Can update user link

            db.session.commit()
            return jsonify(patient.to_dict()), 200
        except ValueError as ve:
            db.session.rollback()
            return jsonify({'error': str(ve)}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Integrity error, e.g., duplicate contact number or user_id, or invalid foreign key'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @role_required(['admin']) # Only Admins can delete patients
    def delete(self, id):
        try:
            patient = Patient.query.get(id)
            if not patient:
                return jsonify({'error': 'Patient not found'}), 404

            db.session.delete(patient)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500