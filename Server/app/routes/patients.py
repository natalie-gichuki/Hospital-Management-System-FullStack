
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource
from app.models import Patient, Outpatient, Inpatient
from app import db
from flask import Blueprint, request, jsonify

class HomeResource(Resource):
    
    def get(self):
        
       response = make_response(jsonify({"message": "Welcome to the Hospital Management System API!"}), 200)
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

        patient_type = data.get('type')

        if patient_type == 'inpatient':
            new_patient = Inpatient(
                name=data['name'],
                age=data['age'],
                gender=data['gender'],
                type='inpatient',
                admission_date=data['admission_date'],
                ward_number=data['ward_number']
            )

        elif patient_type == 'outpatient':
            new_patient = Outpatient(
                name=data['name'],
                age=data['age'],
                gender=data['gender'],
                type='outpatient',
                last_visit_date=data['last_visit_date']
            )

        elif patient_type == 'patient':
            new_patient = Patient(
                name=data['name'],
                age=data['age'],
                gender=data['gender'],
                type='patient'
            )

        else:
            return make_response({'error': 'Invalid patient type'}, 400)

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

