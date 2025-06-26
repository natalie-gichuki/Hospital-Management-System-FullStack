from flask import request, jsonify, make_response
from flask_restful import Resource
from app.models import Department, Doctor
from app import db


class DepartmentList(Resource):
    """Resource for listing and creating departments."""

    def get(self):
        try:
            departments = Department.query.all()
            dept_list = [{
                'id': dept.id,
                'name': dept.name,
                'specialty': dept.specialty,
                'head_doctor_id': dept.head_doctor_id
            } for dept in departments]
            return (dept_list), 200
        except Exception as e:
            db.session.rollback()
            return ({'error': str(e)}), 500

    def post(self):
        try:
            data = request.get_json()

            if not data.get('name') or not data.get('specialty'):
                return ({'error': 'Name and specialty are required'}), 400

            if Department.query.filter_by(name=data['name']).first():
                return ({'error': 'Department with that name already exists'}), 409

            head_doctor_id = data.get('head_doctor_id')
            if head_doctor_id:
                doctor = Doctor.query.get(head_doctor_id)
                if not doctor:
                    return ({'error': 'Head doctor not found'}), 400

            new_dept = Department(
                name=data['name'],
                specialty=data['specialty'],
                head_doctor_id=head_doctor_id
            )

            db.session.add(new_dept)
            db.session.commit()

            return (new_dept.to_dict()), 201
        except Exception as e:
            db.session.rollback()
            return ({'error': str(e)}), 500


class DepartmentByID(Resource):
    """Resource for interacting with a specific department by ID."""

    def get(self, id):
        try:
            dept = Department.query.get(id)
            if not dept:
                return ({'error': 'Department not found'}), 404

            return (dept.to_dict()), 200
        except Exception as e:
            return ({'error': str(e)}), 500

    def patch(self, id):
        try:
            dept = Department.query.get(id)
            if not dept:
                return ({'error': 'Department not found'}), 404

            data = request.get_json()

            if 'name' in data:
                dept.name = data['name']
            if 'specialty' in data:
                dept.specialty = data['specialty']
            if 'head_doctor_id' in data:
                doctor = Doctor.query.get(data['head_doctor_id'])
                if not doctor:
                    return ({'error': 'Invalid doctor ID'}), 400
                dept.head_doctor_id = data['head_doctor_id']

            db.session.commit()
            return (dept.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return ({'error': str(e)}), 500

    def delete(self, id):
        try:
            dept = Department.query.get(id)
            if not dept:
                return ({'error': 'Department not found'}), 404

            db.session.delete(dept)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return ({'error': str(e)}), 500
