from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.models import Doctor, Department
from app import db
from app.routes.auth import role_required
from sqlalchemy.exc import IntegrityError

doctor_ns = Namespace('doctors', description="Doctor resource operations")

# === Swagger Models ===
doctor_model = doctor_ns.model('Doctor', {
    'name': fields.String(required=True, example='Dr. Alice'),
    'specialization': fields.String(required=True, example='Cardiology'),
    'department_id': fields.Integer(required=True, example=1),
    'user_id': fields.Integer(required=False, example=3)
})

update_doctor_model = doctor_ns.model('UpdateDoctor', {
    'name': fields.String(example='Dr. Bob'),
    'specialization': fields.String(example='Dermatology'),
    'department_id': fields.Integer(example=2),
    'user_id': fields.Integer(example=4)
})


@doctor_ns.route('/')
class DoctorList(Resource):

    @role_required(['admin', 'department_manager', 'doctor'])
    @doctor_ns.response(200, 'Success')
    def get(self):
        """Get all doctors"""
        try:
            doctors = Doctor.query.all()
            doctor_list = []
            for doc in doctors:
                doc_dict = doc.to_dict()
                if doc.department:
                    doc_dict['department_name'] = doc.department.name
                doctor_list.append(doc_dict)
            return jsonify(doctor_list)
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @role_required(['admin', 'department_manager'])
    @doctor_ns.expect(doctor_model)
    @doctor_ns.response(201, 'Doctor created successfully')
    @doctor_ns.response(400, 'Missing or invalid data')
    @doctor_ns.response(404, 'Department not found')
    @doctor_ns.response(409, 'Integrity error')
    def post(self):
        """Create a new doctor"""
        try:
            data = request.get_json()
            name = data.get('name')
            specialization = data.get('specialization')
            department_id = data.get('department_id')
            user_id = data.get('user_id')

            if not name or not specialization or not department_id:
                return {'error': 'Name, specialization, and department_id are required'}, 400

            department = Department.query.get(department_id)
            if not department:
                return {'error': 'Department not found'}, 404

            new_doctor = Doctor(
                name=name,
                specialization=specialization,
                department_id=department_id,
                user_id=user_id
            )
            db.session.add(new_doctor)
            db.session.commit()

            return jsonify(new_doctor.to_dict()), 201
        except ValueError as ve:
            db.session.rollback()
            return jsonify({'error': str(ve)}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Integrity error, e.g., duplicate user_id or invalid foreign key'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


@doctor_ns.route('/<int:id>')
class DoctorByID(Resource):

    @role_required(['admin', 'department_manager', 'doctor', 'patient'])
    @doctor_ns.response(200, 'Success')
    @doctor_ns.response(404, 'Doctor not found')
    def get(self, id):
        """Get a doctor by ID"""
        try:
            doctor = Doctor.query.get(id)
            if not doctor:
                return {'error': 'Doctor not found'}, 404

            doc_dict = doctor.to_dict()
            if doctor.department:
                doc_dict['department_name'] = doctor.department.name
            return jsonify(doc_dict)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @role_required(['admin', 'department_manager'])
    @doctor_ns.expect(update_doctor_model)
    @doctor_ns.response(200, 'Doctor updated successfully')
    @doctor_ns.response(404, 'Doctor or department not found')
    @doctor_ns.response(409, 'Conflict: integrity error')
    def patch(self, id):
        """Update a doctor by ID"""
        try:
            doctor = Doctor.query.get(id)
            if not doctor:
                return {'error': 'Doctor not found'}, 404

            data = request.get_json()
            if 'name' in data:
                doctor.name = data['name']
            if 'specialization' in data:
                doctor.specialization = data['specialization']
            if 'department_id' in data:
                department = Department.query.get(data['department_id'])
                if not department:
                    return {'error': 'Department not found'}, 404
                doctor.department_id = data['department_id']
            if 'user_id' in data:
                doctor.user_id = data['user_id']

            db.session.commit()
            return jsonify(doctor.to_dict()), 200
        except ValueError as ve:
            db.session.rollback()
            return jsonify({'error': str(ve)}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Integrity error, e.g., duplicate user_id or invalid foreign key'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @role_required(['admin'])
    @doctor_ns.response(204, 'Doctor deleted')
    @doctor_ns.response(404, 'Doctor not found')
    def delete(self, id):
        """Delete a doctor by ID"""
        try:
            doctor = Doctor.query.get(id)
            if not doctor:
                return {'error': 'Doctor not found'}, 404

            db.session.delete(doctor)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
