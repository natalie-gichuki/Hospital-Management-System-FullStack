from flask import request
from flask_restx import Namespace, Resource, fields
from app.models import Department, Doctor
from app import db
# Removed: from app.routes.auth import role_required # <--- REMOVED THIS IMPORT
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
    def get(self):
        """Get all departments"""
        try:
            departments = Department.query.all()
            rules = ('-doctors', '-headdoctor')
            result = []
            for d in departments:
                dep = d.to_dict(rules=rules)
                # Optionally add summary fields:
                dep['headdoctor_name'] = d.headdoctor.name if hasattr(d, 'headdoctor') and d.headdoctor else None
                result.append(dep)
            return result, 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

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

            rules = ('-doctors', '-headdoctor')
            dep = new_department.to_dict(rules=rules)
            dep['headdoctor_name'] = head_doctor.name if head_doctor else None
            return dep, 201
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
    @department_ns.response(200, 'Success')
    @department_ns.response(404, 'Department not found')
    def get(self, id):
        """Get a department by ID"""
        try:
            department = Department.get_by_id(db.session, id)
            if not department:
                return {'error': 'Department not found'}, 404
            rules = ('-doctors', '-headdoctor')
            dep = department.to_dict(rules=rules)
            dep['headdoctor_name'] = department.headdoctor.name if hasattr(department, 'headdoctor') and department.headdoctor else None
            return dep, 200
        except Exception as e:
            return {'error': str(e)}, 500

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
            rules = ('-doctors', '-headdoctor')
            dep = department.to_dict(rules=rules)
            dep['headdoctor_name'] = department.headdoctor.name if department.headdoctor else None
            return dep, 200
        except ValueError as ve:
            db.session.rollback()
            return {'error': str(ve)}, 400
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Department with this name already exists or invalid data'}, 409
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

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