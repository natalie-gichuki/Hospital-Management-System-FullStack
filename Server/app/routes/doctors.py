
from flask import Blueprint, request, jsonify
from app import db
from app.models import Doctor

doctor_bp = Blueprint('doctor_bp', __name__, url_prefix='/doctors')

@doctor_bp.route('/', methods=['GET'])
def get_all_doctors():
    doctors = Doctor.query.all()
    return jsonify([d.to_dict() for d in doctors]), 200

@doctor_bp.route('/<int:id>', methods=['GET'])
def get_doctor(id):
    doctor = Doctor.query.get(id)
    if doctor:
        return jsonify(doctor.to_dict()), 200
    return jsonify({"error": "Doctor not found"}), 404

@doctor_bp.route('/', methods=['POST'])
def create_doctor():
    data = request.get_json()
    try:
        new_doctor = Doctor(
            name=data['name'],
            specialization=data['specialization'],
            contact=data.get('contact')
            #department_id=data.get('department_id')
        )
        db.session.add(new_doctor)
        db.session.commit()
        return jsonify(new_doctor.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@doctor_bp.route('/<int:id>', methods=['PATCH'])
def update_doctor(id):
    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    data = request.get_json()

    # Include 'contact' so it can be updated from the frontend
    for field in ['name', 'specialization', 'contact', 'department_id']:
        if field in data:
            setattr(doctor, field, data[field])

    db.session.commit()
    return jsonify(doctor.to_dict()), 200


@doctor_bp.route('/<int:id>', methods=['DELETE'])
def delete_doctor(id):
    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    db.session.delete(doctor)
    db.session.commit()
    return jsonify({"message": "Doctor deleted"}), 200
