from flask import request, jsonify
from flask_restful import Resource
from app.models import Doctor, Department
from app import db
from app.routes.auth import role_required # Import our custom role decorator
from sqlalchemy.exc import IntegrityError

class DoctorList(Resource):
    """Resource for listing and creating doctors."""

    @role_required(['admin', 'department_manager', 'doctor']) # Admins, Dept Managers, Doctors can view
    def get(self):
        """
        Get all Doctors
        Retrieves a list of all Doctors.
        ---
        security:
          - BearerAuth: []
        tags:
          - Doctors
        responses:
          200:
            description: A list of doctors.
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  specialty:
                    type: string
                  department_id:
                    type: integer
                  department_name:
                    type: string
                  user_id:
                    type: integer
                  user_username:
                    type: string
                  num_doctors_in_dept:
                    type: integer
          401:
            description: Unauthorized (missing or invalid token).
          403:
            description: Forbidden (insufficient role).
          500:
            description: Internal server error.
        """
        try:
            doctors = Doctor.query.all()
            doctor_list = []
            for doc in doctors:
                doc_dict = doc.to_dict()
                # Add department name for better context in API response
                if doc.department:
                    doc_dict['department_name'] = doc.department.name
                doctor_list.append(doc_dict)
            return jsonify(doctor_list), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @role_required(['admin', 'department_manager']) # Only Admins and Dept Managers can create
    def post(self):
        """
        Create a new Doctor
        Registers a new doctor in the system.
        ---
        security:
          - BearerAuth: []
        tags:
          - Doctors
        parameters:
          - in: body
            name: doctor
            description: Doctor object to be created.
            required: true
            schema:
                type: object
                properties:
                    name:
                        type: string
                        description: Name of the doctor.
                        specialization:
                        type: string
                        description: Specialization of the doctor.
                        department_id:
                        type: integer
                        description: ID of the department the doctor belongs to.
                        user_id:
                        type: integer
                        description: Optional user ID to link the doctor to a specific user.
        responses:
          201:
            description: Doctor has been created successfully.
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                specialization:
                  type: string
                department_id:
                  type: integer
                department_name:
                  type: string
                user_id:
                  type: integer
            400:
                description: Bad request (missing required fields <client-side>).
            404:
                description: Department was not found (invalid department_id is an example cause).
            403:
                description: Forbidden (insufficient role).
            500:
                description: Internal server error.
            """
        try:
            data = request.get_json()

            name = data.get('name')
            specialization = data.get('specialization')
            department_id = data.get('department_id')
            user_id = data.get('user_id') # Optional: link to a User

            if not name or not specialization or not department_id:
                return jsonify({'error': 'Name, specialization, and department_id are required'}), 400

            department = Department.query.get(department_id)
            if not department:
                return jsonify({'error': 'Department not found'}), 404

            new_doctor = Doctor(
                name=name,
                specialization=specialization,
                department_id=department_id,
                user_id=user_id
            )

            db.session.add(new_doctor)
            db.session.commit()

            return jsonify(new_doctor.to_dict()), 201
        except ValueError as ve:
            db.session.rollback()
            return jsonify({'error': str(ve)}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Integrity error, e.g., duplicate user_id or invalid foreign key'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

class DoctorByID(Resource):
    """Resource for interacting with a specific doctor by ID."""

    @role_required(['admin', 'department_manager', 'doctor', 'patient']) # More roles can view specific doctor info
    def get(self, id):
        """
        Get a Doctor by ID
        Retrieves details of a specific doctor by their ID.
        ---
        security:
          - BearerAuth: []
        tags:
          - Doctors
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID of the doctor to retrieve.
        responses:
          200:
            description: Doctor details.
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                specialization:
                  type: string
                department_id:
                  type: integer
                department_name:
                  type: string
                user_id:
                  type: integer
          401:
            description: Unauthorized.
          403:
            description: Forbidden.
          404:
            description: Doctor not found.
            schema:
              type: object
              properties:
                error:
                  type: string
          500:
            description: Internal server error.
        """
        try:
            doctor = Doctor.query.get(id)
            if not doctor:
                return jsonify({'error': 'Doctor not found'}), 404

            doc_dict = doctor.to_dict()
            if doctor.department:
                doc_dict['department_name'] = doctor.department.name

            return jsonify(doc_dict), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @role_required(['admin', 'department_manager']) # Only Admins and Dept Managers can update
    def patch(self, id):
        """
        Update a Doctor by ID
        Updates existing fields of a specific doctor.
        ---
        security:
          - BearerAuth: []
        tags:
          - Doctors
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID of the doctor to update.
          - in: body
            name: body
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: New name for the doctor.
                  example: Dr. Alice Smith
                specialization:
                  type: string
                  description: New specialization for the doctor.
                  example: Pediatric Cardiology
                department_id:
                  type: integer
                  description: New ID of the department the doctor belongs to.
                  example: 2
                user_id:
                  type: integer
                  description: New user ID to link the doctor to.
                  example: 5
        responses:
          200:
            description: Doctor updated successfully.
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                specialization:
                  type: string
                department_id:
                  type: integer
                department_name:
                  type: string
                user_id:
                  type: integer
          400:
            description: Bad request (e.g., validation error, invalid format).
          401:
            description: Unauthorized.
          403:
            description: Forbidden.
          404:
            description: Doctor or Department not found.
          409:
            description: Conflict (e.g., duplicate user_id).
          500:
            description: Internal server error.
        """
        try:
            doctor = Doctor.query.get(id)
            if not doctor:
                return jsonify({'error': 'Doctor not found'}), 404

            data = request.get_json()

            if 'name' in data:
                doctor.name = data['name']
            if 'specialization' in data:
                doctor.specialization = data['specialization']
            if 'department_id' in data:
                department = Department.query.get(data['department_id'])
                if not department:
                    return jsonify({'error': 'Department not found'}), 404
                doctor.department_id = data['department_id']
            if 'user_id' in data:
                doctor.user_id = data['user_id'] # Can update user link

            db.session.commit()
            return jsonify(doctor.to_dict()), 200
        except ValueError as ve:
            db.session.rollback()
            return jsonify({'error': str(ve)}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Integrity error, e.g., duplicate user_id or invalid foreign key'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @role_required(['admin']) # Only Admins can delete doctors
    def delete(self, id):
        """
        Delete a Doctor by ID
        Deletes a specific doctor by their ID.
        ---
        security:
          - BearerAuth: []
        tags:
          - Doctors
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID of the doctor to delete.
        responses:
          204:
            description: Doctor deleted successfully (No Content).
          401:
            description: Unauthorized.
          403:
            description: Forbidden.
          404:
            description: Doctor not found.
            schema:
              type: object
              properties:
                error:
                  type: string
          500:
            description: Internal server error.
        """
        try:
            doctor = Doctor.query.get(id)
            if not doctor:
                return jsonify({'error': 'Doctor not found'}), 404

            db.session.delete(doctor)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500