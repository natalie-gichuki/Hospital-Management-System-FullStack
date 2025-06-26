from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.models import MedicalRecord, Patient, Doctor
from app import db
from app.routes.auth import role_required
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from flask_jwt_extended import current_user

medical_ns = Namespace('medical_records', description="Medical Record operations")

# === Swagger Models ===
medical_record_model = medical_ns.model('MedicalRecord', {
    'patient_id': fields.Integer(required=True, example=1),
    'doctor_id': fields.Integer(required=True, example=2),
    'visit_date': fields.String(required=False, example="2024-04-23T14:00:00"),
    'diagnosis': fields.String(required=True, example="Flu"),
    'treatment': fields.String(required=True, example="Rest and fluids")
})

update_medical_record_model = medical_ns.model('UpdateMedicalRecord', {
    'patient_id': fields.Integer(example=1),
    'doctor_id': fields.Integer(example=2),
    'visit_date': fields.String(example="2024-04-23T14:00:00"),
    'diagnosis': fields.String(example="Flu"),
    'treatment': fields.String(example="Rest and fluids")
})


@medical_ns.route('/')
class MedicalRecordList(Resource):

    @role_required(['admin', 'doctor', 'department_manager'])
    @medical_ns.response(200, "Success")
    def get(self):
        """Get all medical records"""
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
            return jsonify(mr_list)
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @role_required(['admin', 'doctor'])
    @medical_ns.expect(medical_record_model)
    @medical_ns.response(201, 'Medical record created')
    @medical_ns.response(400, 'Invalid input')
    @medical_ns.response(404, 'Patient or Doctor not found')
    def post(self):
        """Create a new medical record"""
        try:
            data = request.get_json()
            patient_id = data.get('patient_id')
            doctor_id = data.get('doctor_id')
            visit_date_str = data.get('visit_date', datetime.utcnow().isoformat())
            diagnosis = data.get('diagnosis')
            treatment = data.get('treatment')

            if not patient_id or not doctor_id or not diagnosis or not treatment:
                return {'error': 'Patient ID, Doctor ID, Diagnosis, and Treatment are required'}, 400

            patient = Patient.query.get(patient_id)
            doctor = Doctor.query.get(doctor_id)
            if not patient:
                return {'error': 'Patient not found'}, 404
            if not doctor:
                return {'error': 'Doctor not found'}, 404

            try:
                visit_date = datetime.fromisoformat(visit_date_str)
            except ValueError:
                return {'error': 'Invalid visit_date format. Use ISO format'}, 400

            new_mr = MedicalRecord(
                patient_id=patient_id,
                doctor_id=doctor_id,
                visit_date=visit_date,
                diagnosis=diagnosis,
                treatment=treatment
            )

            db.session.add(new_mr)
            db.session.commit()
            return jsonify(new_mr.to_dict()), 201
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Integrity error, e.g., invalid foreign key'}, 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


@medical_ns.route('/<int:id>')
class MedicalRecordByID(Resource):

    @role_required(['admin', 'doctor', 'patient', 'department_manager'])
    @medical_ns.response(200, 'Success')
    @medical_ns.response(404, 'Medical record not found')
    def get(self, id):
        """Get a medical record by ID"""
        try:
            medical_record = MedicalRecord.query.get(id)
            if not medical_record:
                return {'error': 'Medical record not found'}, 404

            # Role-based access filtering
            if current_user.role == 'patient' and current_user.patient and current_user.patient.id != medical_record.patient_id:
                return {'msg': 'Access denied: Patients can only view their own records'}, 403
            if current_user.role == 'doctor' and current_user.doctor and current_user.doctor.id != medical_record.doctor_id:
                return {'msg': 'Access denied: Doctors can only view their own created records'}, 403

            mr_dict = medical_record.to_dict()
            if medical_record.patient:
                mr_dict['patient_name'] = medical_record.patient.name
            if medical_record.doctor:
                mr_dict['doctor_name'] = medical_record.doctor.name

            return jsonify(mr_dict)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @role_required(['admin', 'doctor'])
    @medical_ns.expect(update_medical_record_model)
    @medical_ns.response(200, 'Updated successfully')
    @medical_ns.response(404, 'Not found')
    def patch(self, id):
        """Update a medical record by ID"""
        try:
            record = MedicalRecord.query.get(id)
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

            if 'visit_date' in data:
                try:
                    record.visit_date = datetime.fromisoformat(data['visit_date'])
                except ValueError:
                    return {'error': 'Invalid date format'}, 400

            if 'diagnosis' in data:
                record.diagnosis = data['diagnosis']
            if 'treatment' in data:
                record.treatment = data['treatment']

            db.session.commit()
            return jsonify(record.to_dict())
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Integrity error'}, 409
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    @role_required(['admin'])
    @medical_ns.response(204, 'Deleted successfully')
    @medical_ns.response(404, 'Not found')
    def delete(self, id):
        """Delete a medical record by ID"""
        try:
            record = MedicalRecord.query.get(id)
            if not record:
                return {'error': 'Medical record not found'}, 404

            db.session.delete(record)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
