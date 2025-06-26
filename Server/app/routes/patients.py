from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.models import Patient
from app import db
from app.routes.auth import role_required
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from flask_jwt_extended import current_user

patient_ns = Namespace('patients', description="Patient operations")

# === Swagger Models ===
patient_model = patient_ns.model('Patient', {
    'name': fields.String(required=True, example="John Doe"),
    'date_of_birth': fields.String(required=True, example="1990-01-01"),
    'contact_number': fields.String(required=True, example="+254712345678"),
    'user_id': fields.Integer(required=False, example=5),
})

update_patient_model = patient_ns.model('UpdatePatient', {
    'name': fields.String(example="Jane Doe"),
    'date_of_birth': fields.String(example="1992-02-02"),
    'contact_number': fields.String(example="+254700000000"),
    'user_id': fields.Integer(example=7),
})


@patient_ns.route('/')
class PatientList(Resource):

    @role_required(['admin', 'doctor', 'department_manager'])
    @patient_ns.response(200, 'List of patients')
    def get(self):
        """Get all patients"""
        try:
            patients = Patient.query.all()
            return jsonify([p.to_dict() for p in patients])
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    @role_required(['admin', 'department_manager', 'doctor'])
    @patient_ns.expect(patient_model)
    @patient_ns.response(201, 'Patient created')
    @patient_ns.response(400, 'Invalid input')
    @patient_ns.response(409, 'Duplicate contact number')
    def post(self):
        """Create a new patient"""
        try:
            data = request.get_json()
            name = data.get('name')
            dob_str = data.get('date_of_birth')
            contact_number = data.get('contact_number')
            user_id = data.get('user_id')

            if not name or not dob_str or not contact_number:
                return {'error': 'Name, date_of_birth, and contact_number are required'}, 400

            try:
                date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
            except ValueError:
                return {'error': 'Invalid date_of_birth format. Use YYYY-MM-DD'}, 400

            if Patient.query.filter_by(contact_number=contact_number).first():
                return {'error': 'Patient with this contact number already exists'}, 409

            new_patient = Patient(
                name=name,
                date_of_birth=date_of_birth,
                contact_number=contact_number,
                user_id=user_id
            )
            db.session.add(new_patient)
            db.session.commit()
            return jsonify(new_patient.to_dict()), 201
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Integrity error, e.g., duplicate contact number or user_id'}, 409
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500


@patient_ns.route('/<int:id>')
class PatientByID(Resource):

    @role_required(['admin', 'doctor', 'patient', 'department_manager'])
    @patient_ns.response(200, 'Patient details')
    @patient_ns.response(404, 'Patient not found')
    def get(self, id):
        """Get a patient by ID"""
        try:
            patient = Patient.query.get(id)
            if not patient:
                return {'error': 'Patient not found'}, 404

            if current_user.role == 'patient' and current_user.patient and current_user.patient.id != patient.id:
                return {'msg': 'Access denied: Patients can only view their own records'}, 403

            return jsonify(patient.to_dict())
        except Exception as e:
            return {'error': str(e)}, 500

    @role_required(['admin', 'department_manager', 'doctor'])
    @patient_ns.expect(update_patient_model)
    @patient_ns.response(200, 'Patient updated')
    @patient_ns.response(404, 'Patient not found')
    @patient_ns.response(409, 'Conflict: duplicate contact')
    def patch(self, id):
        """Update a patient by ID"""
        try:
            patient = Patient.query.get(id)
            if not patient:
                return {'error': 'Patient not found'}, 404

            data = request.get_json()

            if 'name' in data:
                patient.name = data['name']

            if 'date_of_birth' in data:
                try:
                    patient.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
                except ValueError:
                    return {'error': 'Invalid date_of_birth format. Use YYYY-MM-DD'}, 400

            if 'contact_number' in data:
                existing = Patient.query.filter_by(contact_number=data['contact_number']).first()
                if existing and existing.id != id:
                    return {'error': 'Patient with this contact number already exists'}, 409
                patient.contact_number = data['contact_number']

            if 'user_id' in data:
                patient.user_id = data['user_id']

            db.session.commit()
            return jsonify(patient.to_dict())
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Integrity error'}, 409
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    @role_required(['admin'])
    @patient_ns.response(204, 'Patient deleted')
    @patient_ns.response(404, 'Patient not found')
    def delete(self, id):
        """Delete a patient by ID"""
        try:
            patient = Patient.query.get(id)
            if not patient:
                return {'error': 'Patient not found'}, 404

            db.session.delete(patient)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
