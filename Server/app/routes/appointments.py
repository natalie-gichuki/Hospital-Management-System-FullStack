from flask import Blueprint, request, jsonify
from app import db
from app.models import Appointment, Doctor, Patient

appointment_bp = Blueprint("appointment_bp", __name__, url_prefix="/appointments")

# GET all appointments
@appointment_bp.route("/", methods=["GET"])
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([appt.to_dict() for appt in appointments]), 200

# GET single appointment
@appointment_bp.route("/<int:id>", methods=["GET"])
def get_appointment(id):
    appt = Appointment.query.get(id)
    if appt:
        return jsonify(appt.to_dict()), 200
    return jsonify({"error": "Appointment not found"}), 404

# POST create appointment
@appointment_bp.route("/", methods=["POST"])
def create_appointment():
    data = request.get_json()
    try:
        new_appt = Appointment(
            date=data["date"],
            reason=data["reason"],
            doctor_id=data["doctor_id"],
            patient_id=data["patient_id"]
        )
        db.session.add(new_appt)
        db.session.commit()
        return jsonify(new_appt.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# PATCH update appointment
@appointment_bp.route("/<int:id>", methods=["PATCH"])
def update_appointment(id):
    appt = Appointment.query.get(id)
    if not appt:
        return jsonify({"error": "Appointment not found"}), 404

    data = request.get_json()
    for field in ['date', 'reason', 'doctor_id', 'patient_id']:
        if field in data:
            setattr(appt, field, data[field])

    db.session.commit()
    return jsonify(appt.to_dict()), 200

# DELETE appointment
@appointment_bp.route("/<int:id>", methods=["DELETE"])
def delete_appointment(id):
    appt = Appointment.query.get(id)
    if not appt:
        return jsonify({"error": "Appointment not found"}), 404

    db.session.delete(appt)
    db.session.commit()
    return jsonify({"message": "Appointment deleted"}), 200
