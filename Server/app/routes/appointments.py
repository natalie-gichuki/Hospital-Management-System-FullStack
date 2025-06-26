from flask import request, jsonify
from flask_restful import Resource
from app.models import Appointment, Patient, Doctor
from app import db
from app.routes.auth import role_required
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class AppointmentList(Resource):
    """
    Appointment List Resource
    Manages listing all appointments and creating new ones.
    """

    @role_required(['admin', 'doctor', 'patient', 'department_manager']) # All relevant roles can view appointments
    def get(self):
        """
        Get all Appointments
        Retrieves a list of all appointments.
        ---
        security:
          - BearerAuth: []
        tags:
          - Appointments
        responses:
          200:
            description: A list of appointments.
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  patient_id:
                    type: integer
                  doctor_id:
                    type: integer
                  appointment_date:
                    type: string
                    format: date-time
                  status:
                    type: string
          401:
            description: Unauthorized (missing or invalid token).
          403:
            description: Forbidden (insufficient role).
          500:
            description: Internal server error.
        """
        
        try:
            appointments = Appointment.query.all()
            appointment_list = []
            for appt in appointments:
                appt_dict = appt.to_dict()
                if appt.patient:
                    appt_dict['patient_name'] = appt.patient.name
                    appt_dict['patient_contact'] = appt.patient.contact_number
                if appt.doctor:
                    appt_dict['doctor_name'] = appt.doctor.name
                    appt_dict['doctor_specialization'] = appt.doctor.specialization
                appointment_list.append(appt_dict)
            return jsonify(appointment_list), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @role_required(['admin', 'doctor', 'patient', 'department_manager']) # Any role can potentially create an appointment
    def post(self):
        """
        Create a new Appointment
        Creates a new appointment in the system.
        ---
        security:
          - BearerAuth: []
        tags:
          - Appointments
        parameters:
          - in: body
            name: appointment
            description: Appointment object to be created.
            required: true
            schema:
                type: object
                properties:
                    patient_id:
                        type: integer
                        description: ID of the patient for the appointment.
                    doctor_id:
                        type: integer
                        description: ID of the doctor for the appointment.
                    appointment_date:
                        type: string
                        format: date-time
                        description: Date and time of the appointment (ISO format, e.g., YYYY-MM-DDTHH:MM:SS).
                    status:
                        type: string
                        description: Status of the appointment (e.g., 'Scheduled', 'Completed', 'Canceled'). Defaults to 'Scheduled'.
                        enum: ['Scheduled', 'Completed', 'Canceled']
        responses:
          201:
            description: Appointment has been created successfully.
            schema:
              type: object
              properties:
                id:
                  type: integer
                patient_id:
                  type: integer
                doctor_id:
                  type: integer
                appointment_date:
                  type: string
                  format: date-time
                status:
                  type: string
          400:
            description: Bad request (missing required fields, invalid date format, past date).
          404:
            description: Patient or Doctor not found.
          409:
            description: Conflict (integrity error).
          500:
            description: Internal server error.
        """
        try:
            data = request.get_json()

            patient_id = data.get('patient_id')
            doctor_id = data.get('doctor_id')
            appointment_date_str = data.get('appointment_date') # Expecting ISO format 'YYYY-MM-DDTHH:MM:SS' or similar
            status = data.get('status', 'Scheduled')

            if not patient_id or not doctor_id or not appointment_date_str:
                return jsonify({'error': 'Patient ID, Doctor ID, and Appointment Date are required'}), 400

            patient = Patient.query.get(patient_id)
            doctor = Doctor.query.get(doctor_id)

            if not patient:
                return jsonify({'error': 'Patient not found'}), 404
            if not doctor:
                return jsonify({'error': 'Doctor not found'}), 404

            try:
                # Handle various common datetime formats, ISO preferred
                appointment_date = datetime.fromisoformat(appointment_date_str)
                # Ensure it's not in the past (handled by model validation, but good to check early)
                if appointment_date.replace(tzinfo=None) < datetime.utcnow():
                    return jsonify({'error': 'Appointment date cannot be in the past'}), 400
            except ValueError:
                return jsonify({'error': 'Invalid appointment_date format. Use ISO format (e.g., YYYY-MM-DDTHH:MM:SS)'}), 400

            new_appointment = Appointment(
                patient_id=patient_id,
                doctor_id=doctor_id,
                appointment_date=appointment_date,
                status=status
            )

            db.session.add(new_appointment)
            db.session.commit()

            return jsonify(new_appointment.to_dict()), 201
        except ValueError as ve:
            db.session.rollback()
            return jsonify({'error': str(ve)}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Integrity error, e.g., invalid foreign key'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

class AppointmentByID(Resource):
    """
    Appointment By ID Resource
    Manages retrieving, updating, and deleting a specific appointment.
    """

    @role_required(['admin', 'doctor', 'patient', 'department_manager'])
    def get(self, id):
        """
        Get an Appointment by ID
        Retrieves details of a specific appointment by its ID.
        ---
        security:
          - BearerAuth: []
        tags:
          - Appointments
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID of the appointment to retrieve.
        responses:
          200:
            description: Appointment details.
            schema:
              type: object
              properties:
                id:
                  type: integer
                patient_id:
                  type: integer
                doctor_id:
                  type: integer
                appointment_date:
                  type: string
                  format: date-time
                status:
                  type: string
          401:
            description: Unauthorized.
          403:
            description: Forbidden (e.g., patient/doctor trying to view another's record).
          404:
            description: Appointment not found.
          500:
            description: Internal server error.
        """
        try:
            appointment = Appointment.query.get(id)
            if not appointment:
                return jsonify({'error': 'Appointment not found'}), 404

            # Role-specific access check: Patients/Doctors can only view their own appointments
            from flask_jwt_extended import get_jwt_identity, current_user
            if current_user.role == 'patient' and current_user.patient and current_user.patient.id != appointment.patient_id:
                return jsonify({"msg": "Access denied: Patients can only view their own appointments"}), 403
            if current_user.role == 'doctor' and current_user.doctor and current_user.doctor.id != appointment.doctor_id:
                return jsonify({"msg": "Access denied: Doctors can only view their own appointments"}), 403


            appt_dict = appointment.to_dict()
            if appointment.patient:
                appt_dict['patient_name'] = appointment.patient.name
                appt_dict['patient_contact'] = appointment.patient.contact_number
            if appointment.doctor:
                appt_dict['doctor_name'] = appointment.doctor.name
                appt_dict['doctor_specialization'] = appointment.doctor.specialization

            return jsonify(appt_dict), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @role_required(['admin', 'doctor', 'department_manager']) # Admins, Doctors, Dept Managers can update
    def patch(self, id):
        """
        Update an Appointment by ID
        Updates existing fields of a specific appointment.
        ---
        security:
          - BearerAuth: []
        tags:
          - Appointments
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID of the appointment to update.
          - in: body
            name: body
            schema:
              type: object
              properties:
                patient_id:
                  type: integer
                  description: New patient ID for the appointment.
                doctor_id:
                  type: integer
                  description: New doctor ID for the appointment.
                appointment_date:
                  type: string
                  format: date-time
                  description: New date and time for the appointment (ISO format).
                status:
                  type: string
                  description: New status for the appointment.
                  enum: ['Scheduled', 'Completed', 'Canceled']
        responses:
          200:
            description: Appointment updated successfully.
          400:
            description: Bad request (e.g., validation error, invalid date format, past date).
          401:
            description: Unauthorized.
          403:
            description: Forbidden.
          404:
            description: Appointment, Patient, or Doctor not found.
          409:
            description: Conflict (integrity error).
          500:
            description: Internal server error.
        """
        try:
            appointment = Appointment.query.get(id)
            if not appointment:
                return jsonify({'error': 'Appointment not found'}), 404

            data = request.get_json()

            if 'patient_id' in data:
                patient = Patient.query.get(data['patient_id'])
                if not patient:
                    return jsonify({'error': 'Patient not found'}), 404
                appointment.patient_id = data['patient_id']
            if 'doctor_id' in data:
                doctor = Doctor.query.get(data['doctor_id'])
                if not doctor:
                    return jsonify({'error': 'Doctor not found'}), 404
                appointment.doctor_id = data['doctor_id']
            if 'appointment_date' in data:
                try:
                    new_date = datetime.fromisoformat(data['appointment_date'])
                    if new_date.replace(tzinfo=None) < datetime.utcnow():
                         return jsonify({'error': 'Appointment date cannot be in the past'}), 400
                    appointment.appointment_date = new_date
                except ValueError:
                    return jsonify({'error': 'Invalid appointment_date format. Use ISO format'}), 400
            if 'status' in data:
                appointment.status = data['status'] # Model validation handles valid statuses

            db.session.commit()
            return jsonify(appointment.to_dict()), 200
        except ValueError as ve:
            db.session.rollback()
            return jsonify({'error': str(ve)}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Integrity error, e.g., invalid foreign key'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @role_required(['admin', 'department_manager']) # Only Admins and Dept Managers can delete appointments
    def delete(self, id):
        """
        Delete an Appointment by ID
        Deletes a specific appointment by its ID.
        ---
        security:
          - BearerAuth: []
        tags:
          - Appointments
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID of the appointment to delete.
        responses:
          204:
            description: Appointment deleted successfully (No Content).
          401:
            description: Unauthorized.
          403:
            description: Forbidden.
          404:
            description: Appointment not found.
          500:
            description: Internal server error.
        """
        try:
            appointment = Appointment.query.get(id)
            if not appointment:
                return jsonify({'error': 'Appointment not found'}), 404

            db.session.delete(appointment)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500