from flask import request, jsonify
from flask_restful import Resource
from app.models import Patient
from app import db
from app.routes.auth import role_required # Import our custom role decorator
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class PatientList(Resource):
    """Resource for listing and creating patients."""

    @role_required(['admin', 'doctor', 'department_manager'])
    def get(self):
        """
        Get all Patients
        Retrieves a list of all Patients.
        ---
        security:
          - BearerAuth: []
        tags:
          - Patients
        responses:
          200:
            description: A list of patients.
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  date_of_birth:
                    type: string
                    format: date
                  contact_number:
                    type: string
                  user_id:
                    type: integer
          401:
            description: Unauthorized (missing or invalid token).
          403:
            description: Forbidden (insufficient role).
          500:
            description: Internal server error.
        """
        try:
            patients = Patient.query.all()
            patient_list = [patient.to_dict() for patient in patients]
            return jsonify(patient_list), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @role_required(['admin', 'department_manager', 'doctor'])
    def post(self):
        """
        Create a new Patient
        Registers a new patient in the system.
        ---
        security:
          - BearerAuth: []
        tags:
          - Patients
        parameters:
          - in: body
            name: patient
            description: Patient object to be created.
            required: true
            schema:
                type: object
                properties:
                    name:
                        type: string
                        description: Name of the patient.
                    date_of_birth:
                        type: string
                        format: date
                        description: Date of birth of the patient (YYYY-MM-DD).
                    contact_number:
                        type: string
                        description: Contact number of the patient (must be unique).
                    user_id:
                        type: integer
                        description: Optional user ID to link the patient to a specific user.
        responses:
          201:
            description: Patient has been created successfully.
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                contact_number:
                  type: string
          400:
            description: Bad request (missing required fields, invalid date format).
          409:
            description: Conflict (patient with this contact number already exists).
          500:
            description: Internal server error.
        """
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

    @role_required(['admin', 'doctor', 'patient', 'department_manager'])
    def get(self, id):
        """
        Get a Patient by ID
        Retrieves details of a specific patient by their ID.
        ---
        security:
          - BearerAuth: []
        tags:
          - Patients
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID of the patient to retrieve.
        responses:
          200:
            description: Patient details.
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                date_of_birth:
                  type: string
                  format: date
                contact_number:
                  type: string
                user_id:
                  type: integer
          401:
            description: Unauthorized.
          403:
            description: Forbidden (e.g., patient trying to view another patient's record).
          404:
            description: Patient not found.
          500:
            description: Internal server error.
        """
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

    @role_required(['admin', 'department_manager', 'doctor'])
    def patch(self, id):
        """
        Update a Patient by ID
        Updates existing fields of a specific patient.
        ---
        security:
          - BearerAuth: []
        tags:
          - Patients
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID of the patient to update.
          - in: body
            name: body
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: New name for the patient.
                date_of_birth:
                  type: string
                  format: date
                  description: New date of birth for the patient (YYYY-MM-DD).
                contact_number:
                  type: string
                  description: New contact number for the patient (must be unique).
                user_id:
                  type: integer
                  description: New user ID to link the patient to.
        responses:
          200:
            description: Patient updated successfully.
          400:
            description: Bad request (e.g., validation error, invalid date format).
          401:
            description: Unauthorized.
          403:
            description: Forbidden.
          404:
            description: Patient not found.
          409:
            description: Conflict (e.g., duplicate contact number).
          500:
            description: Internal server error.
        """
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

    @role_required(['admin'])
    def delete(self, id):
        """
        Delete a Patient by ID
        Deletes a specific patient by their ID.
        ---
        security:
          - BearerAuth: []
        tags:
          - Patients
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID of the patient to delete.
        responses:
          204:
            description: Patient deleted successfully (No Content).
          401:
            description: Unauthorized.
          403:
            description: Forbidden.
          404:
            description: Patient not found.
          500:
            description: Internal server error.
        """
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