from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.models import Department, Doctor
from app import db
from app.routes.auth import role_required
from sqlalchemy.exc import IntegrityError

department_ns = Namespace('departments', description="Hospital department operations")

# === Swagger Models ===
department_model = department_ns.model('Department', {
    'name': fields.String(required=True, example='Emergency'),
    'specialty': fields.String(required=True, example='Urgent Care'),
    'head_doctor_id': fields.Integer(required=True, example=1),
})

update_model = department_ns.model('UpdateDepartment', {
    'name': fields.String(example='Pediatrics'),
    'specialty': fields.String(example='Child Healthcare'),
    'head_doctor_id': fields.Integer(example=2),
})


@department_ns.route('/')
class DepartmentList(Resource):

    @role_required(['admin', 'department_manager', 'doctor', 'patient'])
    @department_ns.response(200, 'Success')
    def get(self):
        """Get all departments"""
        try:
            departments = Department.get_all(db.session)
            return jsonify([dept.to_dict() for dept in departments])
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @role_required(['admin', 'department_manager'])
    @department_ns.expect(department_model)
    @department_ns.response(201, 'Department created')
    @department_ns.response(400, 'Missing fields')
    @department_ns.response(404, 'Head doctor not found')
    @department_ns.response(409, 'Department already exists')
    def post(self):
        """Create a new department"""
        try:
            data = request.get_json()
            name = data.get('name')
            specialty = data.get('specialty')
            head_doctor_id = data.get('head_doctor_id')

            if not name or not specialty or not head_doctor_id:
                return {'error': 'Name, specialty, and head_doctor_id are required'}, 400

            head_doctor = Doctor.query.get(head_doctor_id)
            if not head_doctor:
                return {'error': 'Head doctor not found'}, 404

            new_department = Department(name=name, specialty=specialty, head_doctor_id=head_doctor_id)
            new_department.save(db.session)

            return jsonify(new_department.to_dict()), 201
        except ValueError as ve:
            db.session.rollback()
            return {'error': str(ve)}, 400
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Department with this name already exists or invalid data'}, 409
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500


@department_ns.route('/<int:id>')
class DepartmentByID(Resource):

    @role_required(['admin', 'department_manager', 'doctor', 'patient'])
    @department_ns.response(200, 'Success')
    @department_ns.response(404, 'Department not found')
    def get(self, id):
        """Get a department by ID"""
        try:
            department = Department.get_by_id(db.session, id)
            if not department:
                return {'error': 'Department not found'}, 404
            return jsonify(department.to_dict())
        except Exception as e:
            return {'error': str(e)}, 500

    @role_required(['admin', 'department_manager'])
    @department_ns.expect(update_model)
    @department_ns.response(200, 'Updated successfully')
    @department_ns.response(404, 'Department or doctor not found')
    @department_ns.response(409, 'Conflict: duplicate name')
    def patch(self, id):
        """Update a department by ID"""
        try:
            department = Department.get_by_id(db.session, id)
            if not department:
                return {'error': 'Department not found'}, 404

            data = request.get_json()

            if 'name' in data:
                department.name = data['name']
            if 'specialty' in data:
                department.specialty = data['specialty']
            if 'head_doctor_id' in data:
                head_doctor = Doctor.query.get(data['head_doctor_id'])
                if not head_doctor:
                    return {'error': 'Head doctor not found'}, 404
                department.head_doctor_id = data['head_doctor_id']

            db.session.commit()
            return jsonify(department.to_dict()), 200
        except ValueError as ve:
            db.session.rollback()
            return {'error': str(ve)}, 400
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Department with this name already exists or invalid data'}, 409
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    @role_required(['admin'])
    @department_ns.response(204, 'Deleted')
    @department_ns.response(404, 'Department not found')
    def delete(self, id):
        """Delete a department by ID"""
        try:
            department = Department.get_by_id(db.session, id)
            if not department:
                return {'error': 'Department not found'}, 404
            department.delete(db.session)
            return '', 204
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
