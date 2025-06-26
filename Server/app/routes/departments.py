from flask import request, jsonify, make_response
from flask import request, jsonify
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
                'head_doctor_id': dept.head_doctor_id  # Corrected field name
                'specialty': dept.specialty,  # Added missing specialty
                'head_doctor_id': dept.head_doctor_id
            } for dept in departments]
            return make_response(jsonify(dept_list), 200)
            return jsonify(dept_list), 200  # Removed unnecessary make_response
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)
            return jsonify({'error': str(e)}), 500

    def post(self):
        try:
            data = request.get_json()

            if not data.get('name'):
                return make_response({'error': 'Name is required'}, 400)
            if not data.get('name') or not data.get('specialty'):  # Added specialty check
                return jsonify({'error': 'Name and specialty are required'}), 400

            if Department.query.filter_by(name=data['name']).first():
                return make_response({'error': 'Department with that name already exists'}, 409)
                return jsonify({'error': 'Department with that name already exists'}), 409

            if data.get('head_doctor_id'):
                doctor = Doctor.query.get(data['head_doctor_id'])  # Corrected field name
                doctor = Doctor.query.get(data['head_doctor_id'])
                if not doctor:
                    return make_response({'error': 'Head doctor not found'}, 400)
                    return jsonify({'error': 'Head doctor not found'}), 400

            new_dept = Department(
                name=data['name'],
                specialty=data.get('specialty'),
                head_doctor_id=data.get('head_doctor_id')  # Corrected field name
                head_doctor_id=data.get('head_doctor_id')
            )

            db.session.add(new_dept)
            db.session.commit()

            return make_response(jsonify(new_dept.to_dict()), 201)  # Assuming to_dict() method exists
            return jsonify(new_dept.to_dict()), 201  # Keep jsonify for consistency
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)
            return jsonify({'error': str(e)}), 500


class DepartmentByID(Resource):
    """Resource for interacting with a specific department by ID."""

    def get(self, id):
        try:
            dept = Department.query.get(id)
            if not dept:
                return make_response({'error': 'Department not found'}, 404)
                return jsonify({'error': 'Department not found'}), 404

            dept_data = {
                'id': dept.id,
                'name': dept.name,
                'specialty': dept.specialty,
                'head_doctor_id': dept.head_doctor_id  # Corrected field name
                'head_doctor_id': dept.head_doctor_id
            }
            return make_response(jsonify(dept_data), 200)
            return jsonify(dept_data), 200
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)
            return jsonify({'error': str(e)}), 500

    def put(self, id):  # Changed from patch to put for full updates
    def patch(self, id):  # Changed back to patch for partial updates
        try:
            dept = Department.query.get(id)
            if not dept:
                return make_response({'error': 'Department not found'}, 404)
                return jsonify({'error': 'Department not found'}), 404

            data = request.get_json()

            if 'name' in data:
                dept.name = data['name']
            if 'specialty' in data:  # Include specialty in partial updates
                dept.specialty = data['specialty']
            if 'specialty' in data:
                dept.specialty = data['specialty']
            if 'head_doctor_id' in data:  # Corrected field name
                doctor = Doctor.query.get(data['head_doctor_id'])  # Corrected field name
                dept.specialty = data['specialty']
            if 'head_doctor_id' in data:
                doctor = Doctor.query.get(data['head_doctor_id'])
                if not doctor:
                    return make_response({'error': 'Invalid doctor ID'}, 400)
                dept.head_doctor_id = data['head_doctor_id']  # Corrected field name
                    return jsonify({'error': 'Invalid doctor ID'}), 400
                dept.head_doctor_id = data['head_doctor_id']

            db.session.commit()
            return make_response(jsonify(dept.to_dict()), 200)  # Assuming to_dict() method exists
            return jsonify(dept.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)
            return jsonify({'error': str(e)}), 500

    def delete(self, id):
        try:
            dept = Department.query.get(id)
            if not dept:
                return make_response({'error': 'Department not found'}, 404)
                return jsonify({'error': 'Department not found'}), 404

            db.session.delete(dept)
            db.session.commit()
            return make_response({'message': 'Department deleted successfully'}, 204)
            return jsonify({'message': 'Department deleted successfully'}), 204
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error': str(e)}), 500)
            return jsonify({'error': str(e)}), 500
