# app/routes/auth.py (updated with Flasgger docstrings)
from flask import request, jsonify
from flask_restful import Resource
from app.models import User, Doctor, Patient, Department
from app import db, jwt
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, current_user
from sqlalchemy.exc import IntegrityError
from datetime import timedelta

# Callback for loading a user from a JWT
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()

# Decorator to check user roles
def role_required(required_roles):
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            if not current_user:
                return jsonify({"msg": "User not found in token identity"}), 401
            if current_user.role not in required_roles:
                return jsonify({"msg": f"Access denied: Requires one of {', '.join(required_roles)} role(s)"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


class Register(Resource):
    """
    User Registration Endpoint
    Allows new users to register with a username, password, and role.
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: Unique username for the new user.
              example: newuser123
            password:
              type: string
              format: password
              description: Password for the new user.
              example: strongpass
            role:
              type: string
              description: User's role (e.g., 'patient', 'doctor', 'admin', 'department_manager'). Defaults to 'patient'.
              enum: ['admin', 'doctor', 'patient', 'department_manager']
              example: patient
            doctor_id:
              type: integer
              description: Optional ID of the existing doctor to link to this user account (if role is 'doctor').
              example: 1
            patient_id:
              type: integer
              description: Optional ID of the existing patient to link to this user account (if role is 'patient').
              example: 1
    responses:
      201:
        description: User registered successfully.
        schema:
          type: object
          properties:
            message:
              type: string
            user_id:
              type: integer
            role:
              type: string
      400:
        description: Bad request (e.g., missing fields, invalid format).
        schema:
          type: object
          properties:
            error:
              type: string
      409:
        description: Conflict (e.g., username already exists).
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Internal server error.
        schema:
          type: object
          properties:
            error:
              type: string
    """
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            role = data.get('role', 'patient')

            if not username or not password:
                return {'error': 'Username and password are required'}, 400

            if User.query.filter_by(username=username).first():
                return {'error': 'Username already exists'}, 409

            new_user = User(username=username, role=role)
            new_user.password = password

            db.session.add(new_user)
            db.session.commit()

            if role == 'doctor':
                doctor_id = data.get('doctor_id')
                if doctor_id:
                    doctor = Doctor.query.get(doctor_id)
                    if doctor:
                        doctor.user_id = new_user.id
                        db.session.commit()
                    else:
                        return {'message': 'User registered, but doctor ID not found for linking'}, 201
            elif role == 'patient':
                patient_id = data.get('patient_id')
                if patient_id:
                    patient = Patient.query.get(patient_id)
                    if patient:
                        patient.user_id = new_user.id
                        db.session.commit()
                    else:
                        return {'message': 'User registered, but patient ID not found for linking'}, 201

            return {'message': 'User registered successfully', 'user_id': new_user.id, 'role': new_user.role}, 201
        except ValueError as ve:
            db.session.rollback()
            return {'error': str(ve)}, 400
        except IntegrityError:
            db.session.rollback()
            return {'error': 'Username already exists or invalid data'}, 409
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

class Login(Resource):
    """
    User Login Endpoint
    Authenticates a user and returns access and refresh JWT tokens.
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              description: User's username.
              example: admin
            password:
              type: string
              format: password
              description: User's password.
              example: adminpass
    responses:
      200:
        description: Successful login, returns JWT tokens and user role.
        schema:
          type: object
          properties:
            access_token:
              type: string
            refresh_token:
              type: string
            user_role:
              type: string
            user_id:
              type: integer
      400:
        description: Bad request (e.g., missing username/password).
        schema:
          type: object
          properties:
            error:
              type: string
      401:
        description: Unauthorized (invalid credentials).
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Internal server error.
        schema:
          type: object
          properties:
            error:
              type: string
    """
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return {'error': 'Username and password are required'}, 400

            user = User.query.filter_by(username=username).first()
            if not user or not user.verify_password(password):
                return {'error': 'Invalid credentials'}, 401

            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user_role': user.role,
                'user_id': user.id
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500

class RefreshToken(Resource):
    """
    Refresh Access Token Endpoint
    Uses a refresh token to obtain a new access token.
    ---
    security:
      - BearerAuth: []
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Refresh token in the format 'Bearer <refresh_token>'
    responses:
      200:
        description: New access token successfully generated.
        schema:
          type: object
          properties:
            access_token:
              type: string
      401:
        description: Unauthorized (invalid or expired refresh token).
        schema:
          type: object
          properties:
            msg:
              type: string
    """
    @jwt_required(refresh=True)
    def post(self):
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)
        return {'access_token': new_access_token}, 200

class Protected(Resource):
    """
    Protected Example Endpoint
    Accessible by any authenticated user.
    ---
    security:
      - BearerAuth: []
    responses:
      200:
        description: Message confirming authentication and user role.
        schema:
          type: object
          properties:
            msg:
              type: string
      401:
        description: Unauthorized (missing or invalid token).
        schema:
          type: object
          properties:
            msg:
              type: string
    """
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"msg": "User not found"}), 404
        return jsonify({"msg": f"Hello, {user.username}! You are authenticated with role: {user.role}"}), 200

class AdminProtected(Resource):
    """
    Admin Protected Endpoint
    Accessible only by users with the 'admin' role.
    ---
    security:
      - BearerAuth: []
    responses:
      200:
        description: Welcome message for admin.
        schema:
          type: object
          properties:
            msg:
              type: string
      401:
        description: Unauthorized (missing or invalid token).
      403:
        description: Forbidden (insufficient role).
    """
    @role_required(['admin'])
    def get(self):
        return jsonify({"msg": f"Welcome Admin, {current_user.username}! You have full access."}), 200

class DoctorProtected(Resource):
    """
    Doctor Protected Endpoint
    Accessible by users with 'doctor' or 'admin' roles.
    ---
    security:
      - BearerAuth: []
    responses:
      200:
        description: Welcome message for doctor.
        schema:
          type: object
          properties:
            msg:
              type: string
      401:
        description: Unauthorized.
      403:
        description: Forbidden.
    """
    @role_required(['doctor', 'admin'])
    def get(self):
        return jsonify({"msg": f"Welcome Dr. {current_user.username}! Here are your patient records."}), 200

class PatientProtected(Resource):
    """
    Patient Protected Endpoint
    Accessible by users with 'patient' or 'admin' roles.
    ---
    security:
      - BearerAuth: []
    responses:
      200:
        description: Welcome message for patient.
        schema:
          type: object
          properties:
            msg:
              type: string
      401:
        description: Unauthorized.
      403:
        description: Forbidden.
    """
    @role_required(['patient', 'admin'])
    def get(self):
        return jsonify({"msg": f"Welcome Patient {current_user.username}! Here are your appointments."}), 200

class DepartmentManagerProtected(Resource):
    """
    Department Manager Protected Endpoint
    Accessible by users with 'department_manager' or 'admin' roles.
    ---
    security:
      - BearerAuth: []
    responses:
      200:
        description: Welcome message for department manager.
        schema:
          type: object
          properties:
            msg:
              type: string
      401:
        description: Unauthorized.
      403:
        description: Forbidden.
    """
    @role_required(['department_manager', 'admin'])
    def get(self):
        return jsonify({"msg": f"Welcome Department Manager {current_user.username}! Manage departments here."}), 200