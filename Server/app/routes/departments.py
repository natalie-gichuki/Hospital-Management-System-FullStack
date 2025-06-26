# app/routes/departments.py (updated with Flasgger docstrings)
from flask import request, jsonify
from flask_restful import Resource
from app.models import Department, Doctor
from app import db
from app.routes.auth import role_required # Import our custom role decorator
from sqlalchemy.exc import IntegrityError

class DepartmentList(Resource):
    """
    Department List Resource
    Manages listing all departments and creating new ones.
    """

    @role_required(['admin', 'department_manager', 'doctor', 'patient'])
    def get(self):
        """
        Get all Departments
        Retrieves a list of all hospital departments.
        ---
        security:
          - BearerAuth: []
        tags:
          - Departments
        responses:
          200:
            description: A list of departments.
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
                  head_doctor_id:
                    type: integer
                  head_doctor_name:
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
            departments = Department.get_all(db.session)
            department_list = [dept.to_dict() for dept in departments]
            return jsonify(department_list), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @role_required(['admin', 'department_manager'])
    def post(self):
        """
        Create a new Department
        Creates a new department with the given name, specialty, and head doctor.
        ---
        security:
          - BearerAuth: []
        tags:
          - Departments
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - name
                - specialty
                - head_doctor_id
              properties:
                name:
                  type: string
                  description: Name of the department (must be unique).
                  example: Emergency
                specialty:
                  type: string
                  description: Specialty of the department.
                  example: Urgent Care
                head_doctor_id:
                  type: integer
                  description: ID of the doctor who will head this department.
                  example: 1
        responses:
          201:
            description: Department created successfully.
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                specialty:
                  type: string
                head_doctor_id:
                  type: integer
                head_doctor_name:
                  type: string
                num_doctors_in_dept:
                  type: integer
          400:
            description: Bad request (e.g., validation error, missing fields).
            schema:
              type: object
              properties:
                error:
                  type: string
          401:
            description: Unauthorized.
          403:
            description: Forbidden.
          404:
            description: Head doctor not found.
            schema:
              type: object
              properties:
                error:
                  type: string
          409:
            description: Conflict (department with this name already exists).
            schema:
              type: object
              properties:
                error:
                  type: string
          500:
            description: Internal server error.
        """
        try:
            data = request.get_json()

            name = data.get('name')
            specialty = data.get('specialty')
            head_doctor_id = data.get('head_doctor_id')

            if not name or not specialty or not head_doctor_id:
                return jsonify({'error': 'Name, specialty, and head_doctor_id are required'}), 400

            head_doctor = Doctor.query.get(head_doctor_id)
            if not head_doctor:
                return jsonify({'error': 'Head doctor not found'}), 404

            new_department = Department(name=name, specialty=specialty, head_doctor_id=head_doctor_id)
            new_department.save(db.session) # Use the save method defined in the model

            return jsonify(new_department.to_dict()), 201
        except ValueError as ve:
            db.session.rollback()
            return jsonify({'error': str(ve)}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Department with this name already exists or invalid data'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


class DepartmentByID(Resource):
    """
    Department By ID Resource
    Manages retrieving, updating, and deleting a specific department.
    """

    @role_required(['admin', 'department_manager', 'doctor', 'patient'])
    def get(self, id):
        """
        Get a Department by ID
        Retrieves details of a specific department by its ID.
        ---
        security:
          - BearerAuth: []
        tags:
          - Departments
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID of the department to retrieve.
        responses:
          200:
            description: Department details.
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                specialty:
                  type: string
                head_doctor_id:
                  type: integer
                head_doctor_name:
                  type: string
                num_doctors_in_dept:
                  type: integer
          401:
            description: Unauthorized.
          403:
            description: Forbidden.
          404:
            description: Department not found.
            schema:
              type: object
              properties:
                error:
                  type: string
          500:
            description: Internal server error.
        """
        try:
            department = Department.get_by_id(db.session, id)
            if not department:
                return jsonify({'error': 'Department not found'}), 404
            return jsonify(department.to_dict()), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @role_required(['admin', 'department_manager'])
    def patch(self, id):
        """
        Update a Department by ID
        Updates existing fields of a specific department.
        ---
        security:
          - BearerAuth: []
        tags:
          - Departments
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID of the department to update.
          - in: body
            name: body
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: New name for the department (must be unique if changed).
                  example: Pediatrics
                specialty:
                  type: string
                  description: New specialty for the department.
                  example: Child Healthcare
                head_doctor_id:
                  type: integer
                  description: New ID of the doctor to head this department.
                  example: 2
        responses:
          200:
            description: Department updated successfully.
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                specialty:
                  type: string
                head_doctor_id:
                  type: integer
                head_doctor_name:
                  type: string
                num_doctors_in_dept:
                  type: integer
          400:
            description: Bad request (e.g., validation error, invalid format).
          401:
            description: Unauthorized.
          403:
            description: Forbidden.
          404:
            description: Department or new head doctor not found.
          409:
            description: Conflict (department name already exists).
          500:
            description: Internal server error.
        """
        try:
            department = Department.get_by_id(db.session, id)
            if not department:
                return jsonify({'error': 'Department not found'}), 404

            data = request.get_json()

            if 'name' in data:
                department.name = data['name']
            if 'specialty' in data:
                department.specialty = data['specialty']
            if 'head_doctor_id' in data:
                head_doctor = Doctor.query.get(data['head_doctor_id'])
                if not head_doctor:
                    return jsonify({'error': 'Head doctor not found'}), 404
                department.head_doctor_id = data['head_doctor_id']

            db.session.commit()
            return jsonify(department.to_dict()), 200
        except ValueError as ve:
            db.session.rollback()
            return jsonify({'error': str(ve)}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Department with this name already exists or invalid data'}), 409
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @role_required(['admin'])
    def delete(self, id):
        """
        Delete a Department by ID
        Deletes a specific department by its ID.
        ---
        security:
          - BearerAuth: []
        tags:
          - Departments
        parameters:
          - in: path
            name: id
            type: integer
            required: true
            description: ID of the department to delete.
        responses:
          204:
            description: Department deleted successfully (No Content).
          401:
            description: Unauthorized.
          403:
            description: Forbidden.
          404:
            description: Department not found.
            schema:
              type: object
              properties:
                error:
                  type: string
          500:
            description: Internal server error.
        """
        try:
            department = Department.get_by_id(db.session, id)
            if not department:
                return jsonify({'error': 'Department not found'}), 404

            department.delete(db.session) # Use the delete method defined in the model
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500