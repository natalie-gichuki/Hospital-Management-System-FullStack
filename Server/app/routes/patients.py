from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from app.models import Patient
from app import db


class HomeResource(Resource):
    
    def get(self):
        
       response = make_response(jsonify({"message": "Welcome to the Patient API!"}), 200)
       return response
class Patient_List(Resource):

    def get(self):
        patients = [patient.to_dict() for patient in Patient.query.all()]

        patient_list = [{
           'id': patient['id'],
           'name': patient['name'],
           'age': patient['age'],
           'gender': patient['gender'],
           'type': patient['type'],
        }for patient in patients] 

        response = make_response(jsonify(patient_list), 200)

        return response
    
    def post(self):
        data = request.get_json()

        new_patient = Patient(
            name=data['name'],
            age=data['age'],
            gender=data['gender'],
            type=data['type']
        )

        db.session.add(new_patient)
        db.session.commit()

        return make_response(new_patient.to_dict(), 201)

    
class Patient_By_ID(Resource):
    def get(self, id):

        patients = Patient.query.filter_by(id=id).first().to_dict()
        response = make_response(jsonify(patients), 200)
        return response 
    
    def delete(self, id):

        patient = Patient.query.filter_by(id=id).first()

        if not patient:
            return make_response(jsonify({'error': 'Patient does not exist'}))

        db.session.delete(patient)
        db.session.commit()

        return make_response({"message": "Patient Deleted Successfully"}, 204)

class PatientMedicalRecords(Resource):
    def get(self, id):
        patient = Patient.query.get(id)
        if not patient:
            return make_response({"error": "Patient not found"}, 404)

        records = [record.to_dict() for record in patient.medical_records]
        return make_response(records, 200)
