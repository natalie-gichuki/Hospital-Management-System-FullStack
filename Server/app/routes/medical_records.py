from flask import request, jsonify, make_response
from flask_restful import Resource
from app.models import Medical_Record, Patient, Doctor
from app import db


class MedicalRecords(Resource):
    def get(self):
        records = Medical_Record.query.all()

        record_list = [{
            'id': record.id,
            'diagnosis': record.diagnosis,
            'treatment': record.treatment,
            'date': record.date,
            'patient_id': record.patient.id,
            'doctor_id': record.doctor.id
        } for record in records]

        return make_response(jsonify(record_list), 200)
    

    def post(self):
        data = request.get_json()

        # Optional: validate patient and doctor exist
        patient = Patient.query.get(data.get('patient_id'))
        doctor = Doctor.query.get(data.get('doctor_id'))

        if not patient or not doctor:
            return make_response({"error": "Invalid patient or doctor ID"}, 400)

        new_record = Medical_Record(
            diagnosis=data['diagnosis'],
            treatment=data['treatment'],
            date=data['date'],
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id']
        )

        db.session.add(new_record)
        db.session.commit()

        return make_response(new_record.to_dict(), 201)


class MedicalRecordByID(Resource):
    def get(self, id):
        record = Medical_Record.query.get(id)

        if not record:
            return make_response({'error': 'Medical record not found'}, 404)

        record_data = {
            'id': record.id,
            'diagnosis': record.diagnosis,
            'treatment': record.treatment,
            'date': record.date,
            'patient': {
                'id': record.patient.id,
                'name': record.patient.name,
                'age': record.patient.age,
                'gender': record.patient.gender
            },
            'doctor': {
                'id': record.doctor.id,
                'name': record.doctor.name
            }
        }

        return make_response(jsonify(record_data), 200)


    def patch(self, id):
        record = Medical_Record.query.get(id)
        if not record:
            return make_response({'error': 'Medical record not found'}, 404)

        data = request.get_json()
        for attr in ['diagnosis', 'treatment', 'date', 'patient_id', 'doctor_id']:
            if attr in data:
                setattr(record, attr, data[attr])

        db.session.commit()
        return make_response(record.to_dict(), 200)

    def delete(self, id):
        record = Medical_Record.query.get(id)
        if not record:
            return make_response({'error': 'Medical record not found'}, 404)

        db.session.delete(record)
        db.session.commit()
        return make_response({'message': 'Medical record deleted'}, 204)
