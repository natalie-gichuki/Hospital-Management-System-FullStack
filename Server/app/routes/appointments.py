from flask import request
from flask_restx import Namespace, Resource, fields
from app.models import Appointment, Patient, Doctor
from app import db
# Removed: from app.routes.auth import role_required # <--- REMOVED THIS IMPORT
from sqlalchemy.exc import IntegrityError
from datetime import datetime
# Removed: from flask_jwt_extended import current_user, get_jwt_identity # <--- REMOVED THESE IMPORTS

appointments_ns = Namespace('appointments', description="Operations related to Appointments")

# Swagger Models (These remain as they define the API's data structure)
appointment_model = appointments_ns.model('Appointment', {
    'id': fields.Integer(readOnly=True),
    'patient_id': fields.Integer(required=True),
    'doctor_id': fields.Integer(required=True),
    'appointment_date': fields.String(required=True, description="ISO format date-time"),
    'status': fields.String(default='Scheduled', enum=['Scheduled', 'Completed', 'Canceled']),
})

appointment_create_model = appointments_ns.model('AppointmentCreate', {
    'patient_id': fields.Integer(required=True),
    'doctor_id': fields.Integer(required=True),
    'appointment_date': fields.String(required=True, description="ISO format (e.g., 2024-12-31T15:00:00)"),
    'status': fields.String(default='Scheduled', enum=['Scheduled', 'Completed', 'Canceled']),
})


@appointments_ns.route('/')
class AppointmentList(Resource):
    @appointments_ns.doc('get_all_appointments')
    def get(self):
        """Get all appointments"""
        appointments = Appointment.query.all()
        rules = (
            '-patient', '-doctor',  # Prevent recursion by not serializing full related objects
        )
        return [appt.to_dict(rules=rules) for appt in appointments], 200

    @appointments_ns.doc('create_appointment')
    @appointments_ns.expect(appointment_create_model)
    def post(self):
        """Create a new appointment"""
        data = request.get_json()
        try:
            patient_id = data.get('patient_id')
            doctor_id = data.get('doctor_id')
            appointment_date_str = data.get('appointment_date')
            status = data.get('status', 'Scheduled')

            if not patient_id or not doctor_id or not appointment_date_str:
                return {'error': 'Patient ID, Doctor ID, and Appointment Date are required'}, 400

            patient = Patient.query.get(patient_id)
            doctor = Doctor.query.get(doctor_id)

            if not patient:
                return {'error': 'Patient not found'}, 404
            if not doctor:
                return {'error': 'Doctor not found'}, 404

            appointment_date = datetime.fromisoformat(appointment_date_str)
            if appointment_date.replace(tzinfo=None) < datetime.utcnow():
                return {'error': 'Appointment date cannot be in the past'}, 400

            new_appt = Appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                date=appointment_date,
                status=status
            )
            db.session.add(new_appt)
            db.session.commit()
            rules = (
                '-patient.appointments', '-doctor.appointments',
                '-patient.user', '-doctor.user',
                '-patient.medical_records', '-doctor.medical_records'
            )
            return new_appt.to_dict(rules=rules), 201

        except ValueError as ve:
            db.session.rollback()
            return {'error': str(ve)}, 400
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Integrity error, e.g., invalid foreign key'}, 409
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500


@appointments_ns.route('/<int:id>')
@appointments_ns.param('id', 'The Appointment ID')
class AppointmentByID(Resource):
    @appointments_ns.doc('get_appointment_by_id')
    def get(self, id):
        """Get a specific appointment by ID"""
        appointment = Appointment.query.get(id)
        if not appointment:
            return {'error': 'Appointment not found'}, 404
        rules = (
            '-patient.appointments', '-doctor.appointments',
            '-patient.user', '-doctor.user',
            '-patient.medical_records', '-doctor.medical_records'
        )
        return appointment.to_dict(rules=rules), 200

    @appointments_ns.doc('update_appointment')
    @appointments_ns.expect(appointment_create_model)
    def patch(self, id):
        """Update an appointment by ID"""
        appointment = Appointment.query.get(id)
        if not appointment:
            return {'error': 'Appointment not found'}, 404

        data = request.get_json()
        try:
            if 'patient_id' in data:
                patient = Patient.query.get(data['patient_id'])
                if not patient:
                    return {'error': 'Patient not found'}, 404
                appointment.patient_id = data['patient_id']
            if 'doctor_id' in data:
                doctor = Doctor.query.get(data['doctor_id'])
                if not doctor:
                    return {'error': 'Doctor not found'}, 404
                appointment.doctor_id = data['doctor_id']
            if 'appointment_date' in data:
                new_date = datetime.fromisoformat(data['appointment_date'])
                if new_date.replace(tzinfo=None) < datetime.utcnow():
                    return {'error': 'Appointment date cannot be in the past'}, 400
                appointment.date = new_date
            if 'status' in data:
                appointment.status = data['status']

            db.session.commit()
            rules = (
                '-patient.appointments', '-doctor.appointments',
                '-patient.user', '-doctor.user',
                '-patient.medical_records', '-doctor.medical_records'
            )
            return appointment.to_dict(rules=rules), 200

        except ValueError as ve:
            db.session.rollback()
            return {'error': str(ve)}, 400
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Integrity error'}, 409
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    @appointments_ns.doc('delete_appointment')
    def delete(self, id):
        """Delete an appointment by ID"""
        appointment = Appointment.query.get(id)
        if not appointment:
            return {'error': 'Appointment not found'}, 404
        db.session.delete(appointment)
        db.session.commit()
        return '', 204