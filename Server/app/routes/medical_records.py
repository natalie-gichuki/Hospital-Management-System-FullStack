from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
# Ensure this import matches your model class name: Medical_Record
from app.models import Medical_Record, Patient, Doctor, User # Added User for clarity in role logic
from app import db
from app.routes.auth import role_required # Assuming this decorator is correctly implemented
from sqlalchemy.exc import IntegrityError, NoResultFound # Added NoResultFound for explicit checks
from datetime import datetime
from flask_jwt_extended import current_user # Make sure current_user is populated by your JWT setup

medical_ns = Namespace('medical_records', description="Medical Record operations")

# === Swagger Models ===
# The 'date' field will now be expected and returned as an ISO formatted string
# 'status' field added as per your Appointment model (assuming you might want to add it to medical records too, or remove if not)
medical_record_model = medical_ns.model('MedicalRecordInput', { # Renamed to avoid confusion with ORM object
    'patient_id': fields.Integer(required=True, example=1, description="ID of the patient associated with the record."),
    'doctor_id': fields.Integer(required=True, example=2, description="ID of the doctor who created the record."),
    'date': fields.String(required=False, example="2024-04-23T14:00:00", description="Date and time of the medical record (ISO 8601 format). Defaults to current UTC time if not provided."),
    'diagnosis': fields.String(required=True, example="Influenza (Flu)", description="Diagnosis for the patient."),
    'treatment': fields.String(required=True, example="Prescribed Tamiflu, advised rest and fluids.", description="Treatment provided or recommended."),
})

update_medical_record_model = medical_ns.model('UpdateMedicalRecordInput', {
    'patient_id': fields.Integer(example=1, description="New patient ID (optional)."),
    'doctor_id': fields.Integer(example=2, description="New doctor ID (optional)."),
    'date': fields.String(example="2024-04-24T09:30:00", description="New date and time of the medical record (ISO 8601 format, optional)."),
    'diagnosis': fields.String(example="Seasonal Allergy", description="Updated diagnosis (optional)."),
    'treatment': fields.String(example="Antihistamines and nasal spray.", description="Updated treatment (optional)."),
})

# Output model for Swagger documentation (reflects what to_dict() returns)
output_medical_record_model = medical_ns.model('MedicalRecordOutput', {
    'id': fields.Integer(readOnly=True, description="Unique identifier for the medical record."),
    'patient_id': fields.Integer(description="ID of the patient."),
    'doctor_id': fields.Integer(description="ID of the doctor."),
    'date': fields.DateTime(dt_format='iso8601', description="Date and time of the record."), # Use fields.DateTime for output
    'diagnosis': fields.String(description="Diagnosis."),
    'treatment': fields.String(description="Treatment."),
    'patient_name': fields.String(description="Name of the associated patient (if available)."),
    'doctor_name': fields.String(description="Name of the associated doctor (if available)."),
})


@medical_ns.route('/')
class MedicalRecordList(Resource):

    @role_required(['admin', 'doctor', 'patient', 'department_manager']) # Patient added as they might view their own records
    @medical_ns.response(200, "Success", [output_medical_record_model])
    @medical_ns.response(403, "Forbidden")
    @medical_ns.response(500, "Internal Server Error")
    def get(self):
        """Get all medical records (admin/doctor/department_manager) or own records (patient)"""
        try:
            query = Medical_Record.query

            # Implement specific access control based on roles
            if current_user.role == 'patient':
                if not current_user.patient_profile:
                    return {'message': 'User is a patient but has no associated patient profile.'}, 403
                query = query.filter_by(patient_id=current_user.patient_profile.id)
            elif current_user.role == 'doctor':
                if not current_user.doctor_profile:
                    return {'message': 'User is a doctor but has no associated doctor profile.'}, 403
                # Doctors can see records they created or records of patients they are assigned to
                # For simplicity here, they only see records they created, adjust as needed
                query = query.filter_by(doctor_id=current_user.doctor_profile.id)
            # Admin and Department Manager can see all (assuming current query covers this)

            medical_records = query.all()
            mr_list = []
            for mr in medical_records:
                mr_dict = mr.to_dict() # Serialize using SerializerMixin
                if mr.patient:
                    mr_dict['patient_name'] = mr.patient.name
                if mr.doctor:
                    mr_dict['doctor_name'] = mr.doctor.name
                mr_list.append(mr_dict)
            return jsonify(mr_list)
        except Exception as e:
            # db.session.rollback() # Rollback is not necessary for GET requests unless a transaction was started
            print(f"Error fetching medical records: {e}") # Log the error
            return {'error': 'Internal server error: ' + str(e)}, 500

    @role_required(['admin', 'doctor'])
    @medical_ns.expect(medical_record_model)
    @medical_ns.response(201, 'Medical record created', output_medical_record_model)
    @medical_ns.response(400, 'Invalid input')
    @medical_ns.response(404, 'Patient or Doctor not found')
    @medical_ns.response(409, 'Integrity Error (e.g., duplicate entry, foreign key violation)')
    @medical_ns.response(500, "Internal Server Error")
    def post(self):
        """Create a new medical record"""
        try:
            data = request.get_json()
            patient_id = data.get('patient_id')
            doctor_id = data.get('doctor_id')
            # Use 'date' instead of 'visit_date'
            date_str = data.get('date')
            diagnosis = data.get('diagnosis')
            treatment = data.get('treatment')

            # Validate required fields for POST
            if not all([patient_id, doctor_id, diagnosis, treatment]):
                return {'error': 'Patient ID, Doctor ID, Diagnosis, and Treatment are required fields.'}, 400

            # Convert date string to datetime object, default to now if not provided
            record_date = None
            if date_str:
                try:
                    record_date = datetime.fromisoformat(date_str)
                except ValueError:
                    return {'error': 'Invalid date format for "date". Use ISO 8601 format (e.g., YYYY-MM-DDTHH:MM:SS).'}, 400
            else:
                record_date = datetime.utcnow() # Default to current UTC time

            patient = Patient.query.get(patient_id)
            doctor = Doctor.query.get(doctor_id)

            if not patient:
                return {'error': f'Patient with ID {patient_id} not found.'}, 404
            if not doctor:
                return {'error': f'Doctor with ID {doctor_id} not found.'}, 404

            new_mr = Medical_Record( # Use Medical_Record
                patient_id=patient_id,
                doctor_id=doctor_id,
                date=record_date, # Use 'date'
                diagnosis=diagnosis,
                treatment=treatment
            )

            db.session.add(new_mr)
            db.session.commit()
            return jsonify(new_mr.to_dict()), 201 # Return the serialized new record
        except IntegrityError as e:
            db.session.rollback()
            print(f"Integrity Error: {e}")
            return {'error': 'Data integrity issue: could be duplicate entry or invalid foreign key reference.'}, 409
        except ValueError as e: # Catch validation errors from model
            db.session.rollback()
            return {'error': str(e)}, 400
        except Exception as e:
            db.session.rollback()
            print(f"Error creating medical record: {e}")
            return {'error': 'Internal server error: ' + str(e)}, 500


@medical_ns.route('/<int:id>')
class MedicalRecordByID(Resource):

    @role_required(['admin', 'doctor', 'patient', 'department_manager'])
    @medical_ns.response(200, 'Success', output_medical_record_model)
    @medical_ns.response(403, 'Forbidden')
    @medical_ns.response(404, 'Medical record not found')
    @medical_ns.response(500, "Internal Server Error")
    def get(self, id):
        """Get a medical record by ID"""
        try:
            medical_record = Medical_Record.query.get(id) # Use Medical_Record
            if not medical_record:
                return {'error': 'Medical record not found'}, 404

            # Role-based access filtering
            if current_user.role == 'patient':
                if not current_user.patient_profile or current_user.patient_profile.id != medical_record.patient_id:
                    return {'message': 'Access denied: Patients can only view their own records.'}, 403
            elif current_user.role == 'doctor':
                # Doctors can view records they created
                if not current_user.doctor_profile or current_user.doctor_profile.id != medical_record.doctor_id:
                    # Doctors can also view records of patients they treat, even if they didn't create them.
                    # This requires checking if the doctor is associated with the patient's current appointments or historical data.
                    # For simplicity, keeping it to records they created for now.
                    # You might add: or medical_record.patient.appointments.filter_by(doctor_id=current_user.doctor_profile.id).first():
                    return {'message': 'Access denied: Doctors can only view their own created records.'}, 403

            mr_dict = medical_record.to_dict()
            if medical_record.patient:
                mr_dict['patient_name'] = medical_record.patient.name
            if medical_record.doctor:
                mr_dict['doctor_name'] = medical_record.doctor.name

            return jsonify(mr_dict)
        except Exception as e:
            print(f"Error fetching medical record by ID: {e}")
            return {'error': 'Internal server error: ' + str(e)}, 500

    @role_required(['admin', 'doctor'])
    @medical_ns.expect(update_medical_record_model)
    @medical_ns.response(200, 'Updated successfully', output_medical_record_model)
    @medical_ns.response(400, 'Invalid input')
    @medical_ns.response(403, 'Forbidden') # Added for potential access control
    @medical_ns.response(404, 'Not found')
    @medical_ns.response(409, 'Integrity error')
    @medical_ns.response(500, "Internal Server Error")
    def patch(self, id):
        """Update a medical record by ID"""
        try:
            record = Medical_Record.query.get(id) # Use Medical_Record
            if not record:
                return {'error': 'Medical record not found'}, 404

            # Doctors can only update records they created
            if current_user.role == 'doctor' and current_user.doctor_profile and current_user.doctor_profile.id != record.doctor_id:
                return {'message': 'Access denied: Doctors can only update their own created records.'}, 403

            data = request.get_json()

            if 'patient_id' in data:
                patient = Patient.query.get(data['patient_id'])
                if not patient:
                    return {'error': 'Patient not found'}, 404
                record.patient_id = data['patient_id']

            if 'doctor_id' in data:
                doctor = Doctor.query.get(data['doctor_id'])
                if not doctor:
                    return {'error': 'Doctor not found'}, 404
                record.doctor_id = data['doctor_id']

            # Use 'date' instead of 'visit_date'
            if 'date' in data:
                try:
                    record.date = datetime.fromisoformat(data['date']) # Use record.date
                except ValueError:
                    return {'error': 'Invalid date format for "date". Use ISO 8601 format (e.g., YYYY-MM-DDTHH:MM:SS).'}, 400

            if 'diagnosis' in data:
                record.diagnosis = data['diagnosis']
            if 'treatment' in data:
                record.treatment = data['treatment']

            db.session.commit()
            return jsonify(record.to_dict()) # Return updated record
        except IntegrityError as e:
            db.session.rollback()
            print(f"Integrity Error: {e}")
            return {'error': 'Data integrity issue: could be invalid foreign key reference.'}, 409
        except ValueError as e: # Catch validation errors from model
            db.session.rollback()
            return {'error': str(e)}, 400
        except Exception as e:
            db.session.rollback()
            print(f"Error updating medical record: {e}")
            return {'error': 'Internal server error: ' + str(e)}, 500

    @role_required(['admin'])
    @medical_ns.response(204, 'Deleted successfully')
    @medical_ns.response(404, 'Not found')
    @medical_ns.response(500, "Internal Server Error")
    def delete(self, id):
        """Delete a medical record by ID"""
        try:
            record = Medical_Record.query.get(id) # Use Medical_Record
            if not record:
                return {'error': 'Medical record not found'}, 404

            db.session.delete(record)
            db.session.commit()
            return '', 204 # No content for 204
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting medical record: {e}")
            return {'error': 'Internal server error: ' + str(e)}, 500