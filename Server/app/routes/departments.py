from flask import request, jsonify, make_response
from flask_restful import Resource
from app.models import Department, Doctor
from app import db

class DepartmentList(Resource):
    def get(self):
        departments = Department.query.all()
        dept_list = [{
            'id': dept.id,
            'name': dept.name,
            'specialty': dept.specialty,
            'headdoctor': {
                'id': dept.headdoctor.id,
                'name': dept.headdoctor.name,
                'specialization': dept.headdoctor.specialization,
            } if dept.headdoctor else None
        } for dept in departments]
        return make_response(jsonify(dept_list), 200)

    def post(self):
        data = request.get_json()

        if not data.get('name') or not data.get('specialty'):
            return make_response({'error': 'Name and specialty are required'}, 400)

        if Department.query.filter_by(name=data['name']).first():
            return make_response({'error': 'Department with that name already exists'}, 400)

        if data.get('headdoctor_id'):
            doctor = Doctor.query.get(data['headdoctor_id'])
            if not doctor:
                return make_response({'error': 'Head doctor not found'}, 400)

        new_dept = Department(
            name=data['name'],
            specialty=data['specialty'],
            headdoctor_id=data.get('headdoctor_id')
        )

        db.session.add(new_dept)
        db.session.commit()

        return make_response(new_dept.to_dict(), 201)


class DepartmentByID(Resource):
    def get(self, id):
        dept = Department.query.get(id)
        if not dept:
            return make_response({'error': 'Department not found'}, 404)

        dept_data = {
            'id': dept.id,
            'name': dept.name,
            'specialty': dept.specialty,
            'headdoctor': {
                'id': dept.headdoctor.id,
                'name': dept.headdoctor.name,
                'specialization': dept.headdoctor.specialization,
            } if dept.headdoctor else None
        }

        return make_response(dept_data, 200)

    def patch(self, id):
        dept = Department.query.get(id)
        if not dept:
            return make_response({'error': 'Department not found'}, 404)

        data = request.get_json()

        if 'name' in data:
            dept.name = data['name']
        if 'specialty' in data:
            dept.specialty = data['specialty']
        if 'headdoctor_id' in data:
            doctor = Doctor.query.get(data['headdoctor_id'])
            if not doctor:
                return make_response({'error': 'Invalid doctor ID'}, 400)
            dept.headdoctor_id = data['headdoctor_id']

        db.session.commit()
        return make_response({
            'id': dept.id,
            'name': dept.name,
            'specialty': dept.specialty,
            'headdoctor': {
                'id': dept.headdoctor.id,
                'name': dept.headdoctor.name,
                'specialization': dept.headdoctor.specialization,
            } if dept.headdoctor else None
        }, 200)


    def delete(self, id):
        dept = Department.query.get(id)
        if not dept:
            return make_response({'error': 'Department not found'}, 404)

        db.session.delete(dept)
        db.session.commit()
        return make_response({'message': 'Department deleted successfully'}, 204)