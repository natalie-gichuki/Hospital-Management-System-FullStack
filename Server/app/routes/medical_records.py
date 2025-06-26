from flask import request, jsonify
from flask_restful import Resource
from app.models import MedicalRecord, Patient, Doctor
from app import db
from app.routes.auth import role_required
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class MedicalRecordList(Resource):
    """Resource for listing and creating medical records."""

    def get(self):
        """
        Get all Medical Records
        Retrieves a list of all medical records.
        ---
        security:
          - BearerAuth: []
        tags:
          - Medical Records
        responses:
          200:
            description: A list of medical records.
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  patient_id:
                    type: integer
                  patient_name:
                    type: string
                  doctor_id:
                    type: integer
                  doctor_name:
                    type: string
                  visit_date:
                    type: string
                    format: date-time
                  diagnosis:
                    type: string
                  treatment:
                    type: string
          401:
            description: Unauthorized (missing or invalid token).
          403:
            description: Forbidden (insufficient role).
          500:
            description: Internal server error.
        """
    @role_required(['admin', 'doctor', 'department_manager']) # Admins, Doctors, Dept Managers can view
    def get(self):
        try:
            medical_records = MedicalRecord.query.all()
            mr_list = []
            for mr in medical_records:
                mr_dict = mr.to_dict()
                if mr.patient:
                    mr_dict['patient_name'] = mr.patient.name
                if mr.doctor:
                    mr_dict['doctor_name'] = mr.doctor.name
                mr_list.append(mr_dict)
            return jsonify(mr_list), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    def post(self):
        """
        Create a new Medical Record
        Creates a new medical record in the system.
        ---
        security:
          - BearerAuth: []
        tags:
          - Medical Records
        parameters:
          - in: body
            name: medical_record
            description: Medical record object to be created.
            required: true
            schema:
                type: object
                properties:
                    patient_id:
                        type: integer
                        description: ID of the patient.
                    doctor_id:
                        type: integer
                        description: ID of the doctor.
                    visit_date:
                        type: string
                        format: date-time
                        description: Date and time of the visit (ISO format, e.g., YYYY-MM-DDTHH:MM:SS). Defaults to current UTC time.
                    diagnosis:
                        type: string
                        description: Diagnosis for the patient.
                    treatment:
                        type: string
                        description: Treatment provided to the patient.
        responses:
          201:
            description: Medical record has been created successfully.
            schema:
              type: object
              properties:
                id:
                  type: integer
                patient_id:
                  type: integer
                doctor_id:
                  type: integer
                visit_date:
                  type: string
                  format: date-time
                diagnosis:
                  type: string
                treatment:
                  type: string
          400:
            description: Bad request (missing required fields, invalid date format).
          404:
            description: Patient or Doctor not found.
          409:
            description: Conflict (integrity error).
          500:
            description: Internal server error.
        """

    @role_required(['admin', 'doctor']) # Only Admins and Doctors can create medical records
    def post(self):
        try:
            data = request.get_json()

            patient_id = data.get('patient_id')
            doctor_id = data.get('doctor_id')
            visit_date_str = data.get('visit_date', datetime.utcnow().isoformat()) # Default to now
            diagnosis = data.get('diagnosis')
            treatment = data.get('treatment')

            if not patient_id or not doctor_id or not diagnosis or not treatment:
                return jsonify({'error': 'Patient ID, Doctor ID, Diagnosis, and Treatment are required'}), 400

            patient = Patient.query.get(patient_id)
            doctor = Doctor.query.get(doctor_id)

            if not patient:
                return jsonify({'error': 'Patient not found'}), 404
            if not doctor:
                return jsonify({'error': 'Doctor not found'}), 404

            try:
                visit_date = datetime.fromisoformat(visit_date_str)
            except ValueError:
                return jsonify({'error': 'Invalid visit_date format. Use ISO format (e.g., YYYY-MM-DDTHH:MM:SS)'}), 400

            new_medical_record = MedicalRecord(
                patient_id=patient_id,
                doctor_id=doctor_id,
                visit_date=visit_date,
                diagnosis=diagnosis,
                treatment=treatment
            )

            db.session.add(new_medical_record)
            db.session.commit()

            return jsonify(new_medical_record.to_dict()), 201
        except ValueError as ve:
            db.session.rollback()
            return jsonify({'error': str(ve)}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Integrity error, e.g., invalid foreign key'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

class MedicalRecordByID(Resource):
    """Resource for interacting with a specific medical record by ID."""

    def get(self, id):
        """
        Get a Medical Record by ID
        Retrieves details of a specific medical record by its ID.
        ---
        security:
          - BearerAuth: []
        tags:
          - Medical Records
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID of the medical record to retrieve.
        responses:
          200:
            description: Medical record details.
            schema:
              type: object
              properties:
                id:
                  type: integer
                patient_id:
                  type: integer
                patient_name:
                  type: string
                doctor_id:
                  type: integer
                doctor_name:
                  type: string
                visit_date:
                  type: string
                  format: date-time
                diagnosis:
                  type: string
                treatment:
                  type: string
          401:
            description: Unauthorized.
          403:
            description: Forbidden (e.g., patient/doctor trying to view another's record).
          404:
            description: Medical record not found.
          500:
            description: Internal server error.
        """
    @role_required(['admin', 'doctor', 'patient', 'department_manager']) # Admins, Doctors, Patients (their own), Dept Managers can view
    def get(self, id):
        try:
            medical_record = MedicalRecord.query.get(id)
            if not medical_record:
                return jsonify({'error': 'Medical record not found'}), 404

            # Role-specific access check: Patients/Doctors can only view their own related records
            from flask_jwt_extended import get_jwt_identity, current_user
            if current_user.role == 'patient' and current_user.patient and current_user.patient.id != medical_record.patient_id:
                return jsonify({"msg": "Access denied: Patients can only view their own medical records"}), 403
            if current_user.role == 'doctor' and current_user.doctor and current_user.doctor.id != medical_record.doctor_id:
                return jsonify({"msg": "Access denied: Doctors can only view medical records they created"}), 403

            mr_dict = medical_record.to_dict()
            if medical_record.patient:
                mr_dict['patient_name'] = medical_record.patient.name
            if medical_record.doctor:
                mr_dict['doctor_name'] = medical_record.doctor.name

            return jsonify(mr_dict), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def patch(self, id):
        """
        Update a Medical Record by ID
        Updates existing fields of a specific medical record.
        ---
        security:
          - BearerAuth: []
        tags:
          - Medical Records
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID of the medical record to update.
          - in: body
            name: body
            schema:
              type: object
              properties:
                patient_id:
                  type: integer
                  description: New patient ID for the medical record.
                doctor_id:
                  type: integer
                  description: New doctor ID for the medical record.
                visit_date:
                  type: string
                  format: date-time
                  description: New date and time for the visit (ISO format).
                diagnosis:
                  type: string
                  description: New diagnosis for the patient.
                treatment:
                  type: string
                  description: New treatment provided to the patient.
        responses:
          200:
            description: Medical record updated successfully.
          400:
            description: Bad request (e.g., validation error, invalid date format).
          401:
            description: Unauthorized.
          403:
            description: Forbidden.
          404:
            description: Medical record, Patient, or Doctor not found.
          409:
            description: Conflict (integrity error).
          500:
            description: Internal server error.
        """
    @role_required(['admin', 'doctor']) # Only Admins and Doctors can update medical records
    def patch(self, id):
        try:
            medical_record = MedicalRecord.query.get(id)
            if not medical_record:
                return jsonify({'error': 'Medical record not found'}), 404

            data = request.get_json()

            if 'patient_id' in data:
                patient = Patient.query.get(data['patient_id'])
                if not patient:
                    return jsonify({'error': 'Patient not found'}), 404
                medical_record.patient_id = data['patient_id']
            if 'doctor_id' in data:
                doctor = Doctor.query.get(data['doctor_id'])
                if not doctor:
                    return jsonify({'error': 'Doctor not found'}), 404
                medical_record.doctor_id = data['doctor_id']
            if 'visit_date' in data:
                try:
                    medical_record.visit_date = datetime.fromisoformat(data['visit_date'])
                except ValueError:
                    return jsonify({'error': 'Invalid visit_date format. Use ISO format'}), 400
            if 'diagnosis' in data:
                medical_record.diagnosis = data['diagnosis']
            if 'treatment' in data:
                medical_record.treatment = data['treatment']

            db.session.commit()
            return jsonify(medical_record.to_dict()), 200
        except ValueError as ve:
            db.session.rollback()
            return jsonify({'error': str(ve)}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Integrity error, e.g., invalid foreign key'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    def delete(self, id):
        """
        Delete a Medical Record by ID
        Deletes a specific medical record by its ID.
        ---
        security:
          - BearerAuth: []
        tags:
          - Medical Records
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID of the medical record to delete.
        responses:
          204:
            description: Medical record deleted successfully (No Content).
          401:
            description: Unauthorized.
          403:
            description: Forbidden.
          404:
            description: Medical record not found.
          500:
            description: Internal server error.
        """

    @role_required(['admin']) # Only Admins can delete medical records
    def delete(self, id):
        try:
            medical_record = MedicalRecord.query.get(id)
            if not medical_record:
                return jsonify({'error': 'Medical record not found'}), 404

            db.session.delete(medical_record)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500