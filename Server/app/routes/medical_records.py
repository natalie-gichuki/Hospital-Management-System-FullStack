from flask import request
from flask_restx import Namespace, Resource, fields
# Ensure this import matches your model class name: Medical_Record
from app.models import Medical_Record, Patient, Doctor, User
from app import db
# Removed: from app.routes.auth import role_required # <--- REMOVED THIS IMPORT
from sqlalchemy.exc import IntegrityError, NoResultFound
from datetime import datetime
# Removed: from flask_jwt_extended import current_user # <--- REMOVED THIS IMPORT

medical_ns = Namespace('medical_records', description="Medical Record operations")

# === Swagger Models ===
# These models remain as they define the API's data structure
medical_record_model = medical_ns.model('MedicalRecordInput', {
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

output_medical_record_model = medical_ns.model('MedicalRecordOutput', {
    'id': fields.Integer(readOnly=True, description="Unique identifier for the medical record."),
    'patient_id': fields.Integer(description="ID of the patient."),
    'doctor_id': fields.Integer(description="ID of the doctor."),
    'date': fields.DateTime(dt_format='iso8601', description="Date and time of the record."),
    'diagnosis': fields.String(description="Diagnosis."),
    'treatment': fields.String(description="Treatment."),
    'patient_name': fields.String(description="Name of the associated patient (if available)."),
    'doctor_name': fields.String(description="Name of the associated doctor (if available)."),
})


@medical_ns.route('/')
class MedicalRecordList(Resource):
    def get(self):
        """Get all medical records"""
        try:
            records = Medical_Record.query.all()
            rules = ('-patient', '-doctor')
            result = []
            for r in records:
                rec = r.to_dict(rules=rules)
                # Optionally add summary fields:
                rec['patient_name'] = r.patient.name if r.patient else None
                rec['doctor_name'] = r.doctor.name if r.doctor else None
                result.append(rec)
            return result, 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    @medical_ns.expect(medical_record_model)
    @medical_ns.response(201, 'Medical record created')
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
            date_str = data.get('date')
            diagnosis = data.get('diagnosis')
            treatment = data.get('treatment')

            if not all([patient_id, doctor_id, diagnosis, treatment]):
                return {'error': 'Patient ID, Doctor ID, Diagnosis, and Treatment are required fields.'}, 400

            record_date = None
            if date_str:
                try:
                    record_date = datetime.fromisoformat(date_str)
                except ValueError:
                    return {'error': 'Invalid date format for "date". Use ISO 8601 format (e.g., YYYY-MM-DDTHH:MM:SS).'}, 400
            else:
                record_date = datetime.utcnow()

            patient = Patient.query.get(patient_id)
            doctor = Doctor.query.get(doctor_id)

            if not patient:
                return {'error': f'Patient with ID {patient_id} not found.'}, 404
            if not doctor:
                return {'error': f'Doctor with ID {doctor_id} not found.'}, 404

            new_mr = Medical_Record(
                patient_id=patient_id,
                doctor_id=doctor_id,
                date=record_date,
                diagnosis=diagnosis,
                treatment=treatment
            )

            db.session.add(new_mr)
            db.session.commit()
            rules = (
                '-patient.medical_records', '-doctor.medical_records',
                '-patient.user', '-doctor.user'
            )
            rec = new_mr.to_dict(rules=rules)
            rec['patient_name'] = patient.name if patient else None
            rec['doctor_name'] = doctor.name if doctor else None
            return rec, 201
        except IntegrityError as e:
            db.session.rollback()
            print(f"Integrity Error: {e}")
            return {'error': 'Data integrity issue: could be duplicate entry or invalid foreign key reference.'}, 409
        except ValueError as e:
            db.session.rollback()
            return {'error': str(e)}, 400
        except Exception as e:
            db.session.rollback()
            print(f"Error creating medical record: {e}")
            return {'error': 'Internal server error: ' + str(e)}, 500


@medical_ns.route('/<int:id>')
class MedicalRecordByID(Resource):
    @medical_ns.response(200, 'Success')
    @medical_ns.response(404, 'Medical record not found')
    @medical_ns.response(500, "Internal Server Error")
    def get(self, id):
        """Get a medical record by ID"""
        try:
            medical_record = Medical_Record.query.get(id)
            if not medical_record:
                return {'error': 'Medical record not found'}, 404

            rules = (
                '-patient.medical_records', '-doctor.medical_records',
                '-patient.user', '-doctor.user'
            )
            mr_dict = medical_record.to_dict(rules=rules)
            mr_dict['patient_name'] = medical_record.patient.name if medical_record.patient else None
            mr_dict['doctor_name'] = medical_record.doctor.name if medical_record.doctor else None

            return mr_dict, 200
        except Exception as e:
            print(f"Error fetching medical record by ID: {e}")
            return {'error': 'Internal server error: ' + str(e)}, 500

    @medical_ns.expect(update_medical_record_model)
    @medical_ns.response(200, 'Updated successfully')
    @medical_ns.response(400, 'Invalid input')
    @medical_ns.response(404, 'Not found')
    @medical_ns.response(409, 'Integrity error')
    @medical_ns.response(500, "Internal Server Error")
    def patch(self, id):
        """Update a medical record by ID"""
        try:
            record = Medical_Record.query.get(id)
            if not record:
                return {'error': 'Medical record not found'}, 404

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

            if 'date' in data:
                try:
                    record.date = datetime.fromisoformat(data['date'])
                except ValueError:
                    return {'error': 'Invalid date format for "date". Use ISO 8601 format (e.g., YYYY-MM-DDTHH:MM:SS).'}, 400

            if 'diagnosis' in data:
                record.diagnosis = data['diagnosis']
            if 'treatment' in data:
                record.treatment = data['treatment']

            db.session.commit()
            rules = (
                '-patient.medical_records', '-doctor.medical_records',
                '-patient.user', '-doctor.user'
            )
            rec = record.to_dict(rules=rules)
            rec['patient_name'] = record.patient.name if record.patient else None
            rec['doctor_name'] = record.doctor.name if record.doctor else None
            return rec, 200
        except IntegrityError as e:
            db.session.rollback()
            print(f"Integrity Error: {e}")
            return {'error': 'Data integrity issue: could be invalid foreign key reference.'}, 409
        except ValueError as e:
            db.session.rollback()
            return {'error': str(e)}, 400
        except Exception as e:
            db.session.rollback()
            print(f"Error updating medical record: {e}")
            return {'error': 'Internal server error: ' + str(e)}, 500

    @medical_ns.response(204, 'Deleted successfully')
    @medical_ns.response(404, 'Not found')
    @medical_ns.response(500, "Internal Server Error")
    def delete(self, id):
        """Delete a medical record by ID"""
        try:
            record = Medical_Record.query.get(id)
            if not record:
                return {'error': 'Medical record not found'}, 404

            db.session.delete(record)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting medical record: {e}")
            return {'error': 'Internal server error: ' + str(e)}, 500