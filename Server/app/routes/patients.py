from flask import Blueprint, request, jsonify
from app.models import Patient
from app import db

patient_bp = Blueprint('patients', __name__)

@patient_bp.route('/patients/', methods=['GET'])
def get_patients():
    patients = Patient.query.all()
    return jsonify([p.to_dict() for p in patients]), 200

