from flask import request
from flask_restx import Namespace, Resource, fields
from app.models import Patient
from app import db
# Removed: from app.routes.auth import role_required # <--- REMOVED THIS IMPORT
from sqlalchemy.exc import IntegrityError
from datetime import datetime
# Removed: from flask_jwt_extended import current_user # <--- REMOVED THIS IMPORT

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

    # Removed: @role_required(['admin', 'doctor', 'department_manager']) # <--- REMOVED THIS DECORATOR
    @patient_ns.response(200, 'List of patients')
    @patient_ns.marshal_list_with(patient_model)
    def get(self):
        """Get all patients"""
        try:
            patients = Patient.query.all()
            return [p.to_dict() for p in patients], 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    # Removed: @role_required(['admin', 'department_manager', 'doctor']) # <--- REMOVED THIS DECORATOR
    @patient_ns.expect(patient_model)
    @patient_ns.response(201, 'Patient created')
    @patient_ns.response(400, 'Invalid input')
    @patient_ns.response(409, 'Duplicate contact number')
    @patient_ns.marshal_with(patient_model, code=201)
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

            # The check for duplicate contact number is a good database-level constraint
            # and doesn't rely on JWT, so it remains.
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
            return new_patient.to_dict(), 201
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Integrity error, e.g., duplicate contact number or user_id'}, 409
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500


@patient_ns.route('/<int:id>')
class PatientByID(Resource):

    # Removed: @role_required(['admin', 'doctor', 'patient', 'department_manager']) # <--- REMOVED THIS DECORATOR
    @patient_ns.response(200, 'Patient details')
    @patient_ns.response(404, 'Patient not found')
    @patient_ns.marshal_with(patient_model)
    def get(self, id):
        """Get a patient by ID"""
        try:
            patient = Patient.query.get(id)
            if not patient:
                return {'error': 'Patient not found'}, 404

            # Removed current_user-based access check as there is no JWT
            # if current_user.role == 'patient' and current_user.patient_profile and current_user.patient_profile.id != patient.id:
            #     return {'msg': 'Access denied: Patients can only view their own records'}, 403

            return patient.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 500

    # Removed: @role_required(['admin', 'department_manager', 'doctor']) # <--- REMOVED THIS DECORATOR
    @patient_ns.expect(update_patient_model)
    @patient_ns.response(200, 'Patient updated')
    @patient_ns.response(404, 'Patient not found')
    @patient_ns.response(409, 'Conflict: duplicate contact')
    @patient_ns.marshal_with(patient_model)
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
            return patient.to_dict(), 200
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Integrity error'}, 409
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    # Removed: @role_required(['admin']) # <--- REMOVED THIS DECORATOR
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