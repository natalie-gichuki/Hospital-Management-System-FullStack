# to handle user registration, login and token management.
# app/routes/auth.py
from flask import request, jsonify
from flask_restful import Resource
from app.models import User, Doctor, Patient, Department
from app import db, jwt
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, current_user
from sqlalchemy.exc import IntegrityError
from datetime import timedelta

# Callback for loading a user from a JWT
# This function is used by @jwt_required() to load the identity from the token
# It's not strictly necessary for the basic login flow, but good for custom user loading
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()

# Decorator to check user roles
def role_required(required_roles):
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            # current_user is available due to @jwt.user_lookup_loader
            if not current_user:
                return jsonify({"msg": "User not found in token identity"}), 401
            if current_user.role not in required_roles:
                return jsonify({"msg": f"Access denied: Requires one of {', '.join(required_roles)} role(s)"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


class Register(Resource):
    """User registration endpoint."""
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            role = data.get('role', 'patient') # Default role is 'patient'

            if not username or not password:
                return {'error': 'Username and password are required'}, 400

            if User.query.filter_by(username=username).first():
                return {'error': 'Username already exists'}, 409

            new_user = User(username=username, role=role)
            new_user.password = password # This uses the setter to hash the password

            db.session.add(new_user)
            db.session.commit()

            # If the role is doctor or patient, link the user to an existing entity or create a placeholder
            if role == 'doctor':
                doctor_id = data.get('doctor_id')
                if doctor_id:
                    doctor = Doctor.query.get(doctor_id)
                    if doctor:
                        doctor.user_id = new_user.id
                        db.session.commit()
                    else:
                        return {'message': 'User registered, but doctor ID not found for linking'}, 201
                else: # Optional: Create a placeholder doctor if no ID is provided
                    # You might want to enforce doctor_id for doctor roles
                    pass
            elif role == 'patient':
                patient_id = data.get('patient_id')
                if patient_id:
                    patient = Patient.query.get(patient_id)
                    if patient:
                        patient.user_id = new_user.id
                        db.session.commit()
                    else:
                        return {'message': 'User registered, but patient ID not found for linking'}, 201
                else: # Optional: Create a placeholder patient if no ID is provided
                    # You might want to enforce patient_id for patient roles
                    pass

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
    """User login endpoint."""
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
    """Endpoint for refreshing access tokens using a refresh token."""
    @jwt_required(refresh=True) # Requires a refresh token
    def post(self):
        current_user_id = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_id)
        return {'access_token': new_access_token}, 200

class Protected(Resource):
    """Example of a protected endpoint accessible only by authenticated users."""
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"msg": "User not found"}), 404
        return jsonify({"msg": f"Hello, {user.username}! You are authenticated with role: {user.role}"}), 200

class AdminProtected(Resource):
    """Example of an endpoint accessible only by 'admin' role."""
    @role_required(['admin'])
    def get(self):
        return jsonify({"msg": f"Welcome Admin, {current_user.username}! You have full access."}), 200

class DoctorProtected(Resource):
    """Example of an endpoint accessible only by 'doctor' role."""
    @role_required(['doctor', 'admin']) # Admins can also access doctor routes
    def get(self):
        return jsonify({"msg": f"Welcome Dr. {current_user.username}! Here are your patient records."}), 200

class PatientProtected(Resource):
    """Example of an endpoint accessible only by 'patient' role."""
    @role_required(['patient', 'admin']) # Admins can also access patient routes
    def get(self):
        return jsonify({"msg": f"Welcome Patient {current_user.username}! Here are your appointments."}), 200

class DepartmentManagerProtected(Resource):
    """Example of an endpoint accessible only by 'department_manager' role."""
    @role_required(['department_manager', 'admin']) # Admins can also access department manager routes
    def get(self):
        return jsonify({"msg": f"Welcome Department Manager {current_user.username}! Manage departments here."}), 200