from flask import request
from flask_restx import Namespace, Resource, fields
from app.models import Patient
from app import db
from sqlalchemy.exc import IntegrityError

patient_ns = Namespace('patients', description="Patient operations")

# === Swagger Models ===
patient_model = patient_ns.model('Patient', {
    'name': fields.String(required=True, example="John Doe"),
    'age': fields.Integer(required=True, example=30),
    'gender': fields.String(required=True, example="male"),
    'user_id': fields.Integer(required=True, example=5)
})

update_patient_model = patient_ns.model('UpdatePatient', {
    'name': fields.String(example="Jane Doe"),
    'age': fields.Integer(example=35),
    'gender': fields.String(example="female"),
    'user_id': fields.Integer(example=7)
})


@patient_ns.route('/')
class PatientList(Resource):

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

    @patient_ns.expect(patient_model)
    @patient_ns.response(201, 'Patient created')
    @patient_ns.response(400, 'Invalid input')
    @patient_ns.marshal_with(patient_model, code=201)
    def post(self):
        """Create a new patient"""
        try:
            data = request.get_json()

            name = data.get('name')
            age = data.get('age')
            gender = data.get('gender')
            user_id = data.get('user_id')

            if not name or age is None or not gender:
                return {'error': 'Name, age, and gender are required'}, 400

            normalized_gender = gender.lower().strip()
            if normalized_gender not in ['male', 'female', 'other']:
                return {'error': 'Gender must be male, female, or other'}, 400

            new_patient = Patient(
                name=name.strip(),
                age=age,
                gender=normalized_gender,
                user_id=user_id
            )

            db.session.add(new_patient)
            db.session.commit()
            return new_patient.to_dict(), 201

        except IntegrityError:
            db.session.rollback()
            return {'error': 'User ID must be unique or already in use'}, 409
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500


@patient_ns.route('/<int:id>')
class PatientByID(Resource):

    @patient_ns.response(200, 'Patient details')
    @patient_ns.response(404, 'Patient not found')
    @patient_ns.marshal_with(patient_model)
    def get(self, id):
        """Get a patient by ID"""
        try:
            patient = Patient.query.get(id)
            if not patient:
                return {'error': 'Patient not found'}, 404

            return patient.to_dict(), 200
        except Exception as e:
            return {'error': str(e)}, 500

    @patient_ns.expect(update_patient_model)
    @patient_ns.response(200, 'Patient updated')
    @patient_ns.response(404, 'Patient not found')
    @patient_ns.response(409, 'Conflict: duplicate user ID')
    @patient_ns.marshal_with(patient_model)
    def patch(self, id):
        """Update a patient by ID"""
        try:
            patient = Patient.query.get(id)
            if not patient:
                return {'error': 'Patient not found'}, 404

            data = request.get_json()

            if 'name' in data:
                patient.name = data['name'].strip()

            if 'age' in data:
                patient.age = data['age']

            if 'gender' in data:
                gender = data['gender'].lower().strip()
                if gender not in ['male', 'female', 'other']:
                    return {'error': 'Invalid gender'}, 400
                patient.gender = gender

            if 'user_id' in data:
                # Ensure no one else is using this user_id
                existing = Patient.query.filter_by(user_id=data['user_id']).first()
                if existing and existing.id != id:
                    return {'error': 'User ID already in use'}, 409
                patient.user_id = data['user_id']

            db.session.commit()
            return patient.to_dict(), 200

        except IntegrityError:
            db.session.rollback()
            return {'error': 'Integrity error'}, 409
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

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
