# app/routes/auth.py
from flask import request # Removed jsonify as it's not directly used with Flask-RESTx marshalling
from flask_restx import Namespace, Resource, fields
from app.models import User, Doctor, Patient # Assuming Patient and Doctor models are needed for profile linking
from app import db # Assuming your db instance is imported from app
# Removed: from app import db, jwt # Removed 'jwt' import
# Removed all flask_jwt_extended imports:
# from flask_jwt_extended import (
#     create_access_token,
#     create_refresh_token,
#     jwt_required,
#     get_jwt_identity,
#     current_user
# )
# Removed: from datetime import timedelta
from sqlalchemy.exc import IntegrityError
# Removed: from flask_jwt_extended.exceptions import NoAuthorizationError


auth_ns = Namespace('auth', description="Authentication and authorization operations")

# Removed JWT user loader and role_required decorator
# @jwt.user_lookup_loader
# def user_lookup_callback(_jwt_header, jwt_data):
#     identity = jwt_data["sub"]
#     return User.query.filter_by(id=int(identity)).first()

# Removed:
# def role_required(required_roles):
#     def wrapper(fn):
#         @jwt_required()
#         def decorator(*args, **kwargs):
#             try:
#                 if not current_user:
#                     return {"msg": "User not found in token identity. Please log in again."}, 401
#                 if current_user.role not in required_roles:
#                     return {"msg": f"Access denied: Your role ({current_user.role}) is not authorized. Requires one of {', '.join(required_roles)}."}, 403
#                 return fn(*args, **kwargs)
#             except NoAuthorizationError as e:
#                 return {"msg": "Authorization token is missing or invalid. Please log in."}, 401
#             except Exception as e:
#                 print(f"Error in role_required decorator: {e}")
#                 return {"msg": f"An unexpected server error occurred: {str(e)}"}, 500
#         return decorator
#     return wrapper


# Models for Swagger (updated to remove JWT-specific fields)
register_model = auth_ns.model('Register', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'role': fields.String(default='patient', enum=['admin', 'doctor', 'patient', 'department_manager']),
    'doctor_id': fields.Integer(required=False), # Still relevant if you link user to doctor/patient profile
    'patient_id': fields.Integer(required=False) # Still relevant if you link user to doctor/patient profile
})

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

# Removed token_response model as we're not returning tokens anymore
# token_response = auth_ns.model('TokenResponse', {
#     'access_token': fields.String(),
#     'refresh_token': fields.String(),
#     'user_role': fields.String(),
#     'user_id': fields.Integer()
# })

# A simpler response model for successful login/registration
auth_success_response = auth_ns.model('AuthSuccessResponse', {
    'message': fields.String(description='Success message'),
    'user_id': fields.Integer(description='ID of the user'),
    'user_role': fields.String(description='Role of the user'),
    'username': fields.String(description='Username of the user')
})


@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    @auth_ns.response(201, 'User registered successfully', auth_success_response) # Changed response model
    @auth_ns.response(400, 'Missing or invalid data')
    @auth_ns.response(409, 'Username already exists')
    def post(self):
        """Register a new user"""
        data = request.get_json()
        try:
            username = data.get('username')
            password = data.get('password')
            role = data.get('role', 'patient')

            if not username or not password:
                return {'error': 'Username and password are required'}, 400

            if User.query.filter_by(username=username).first():
                return {'error': 'Username already exists'}, 409

            new_user = User(username=username, role=role)
            new_user.password = password # This will hash the password via the setter
            db.session.add(new_user)
            db.session.commit() # Commit to get user ID

            # Link to Doctor/Patient profile if provided AFTER new_user gets an ID
            # NOTE: For a real app without JWT, you'd need a way to assign a user_id to an existing
            # doctor/patient, or create the profile along with the user registration.
            # This logic should be carefully designed. For now, assuming direct linkage.
            if role == 'doctor' and data.get('doctor_id'):
                doctor = Doctor.query.get(data['doctor_id'])
                if doctor:
                    doctor.user_id = new_user.id
                    db.session.commit()
                else:
                    print(f"Warning: Doctor ID {data['doctor_id']} not found for new user {new_user.username}")
            elif role == 'patient' and data.get('patient_id'):
                patient = Patient.query.get(data['patient_id'])
                if patient:
                    patient.user_id = new_user.id
                    db.session.commit()
                else:
                    print(f"Warning: Patient ID {data['patient_id']} not found for new user {new_user.username}")

            # Removed access_token and refresh_token generation
            return {
                'message': 'User registered successfully',
                'user_id': new_user.id,
                'user_role': new_user.role, # Renamed from 'role' for consistency with login
                'username': new_user.username
            }, 201

        except IntegrityError:
            db.session.rollback()
            return {'error': 'Username already exists or invalid data provided'}, 409
        except ValueError as ve:
            db.session.rollback()
            return {'error': str(ve)}, 400
        except Exception as e:
            db.session.rollback()
            print(f"Error during user registration: {e}")
            return {'error': str(e)}, 500


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.response(200, 'Login successful', auth_success_response) # Changed response model
    @auth_ns.response(401, 'Invalid credentials')
    def post(self):
        """Login and get user details (no tokens)"""
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'error': 'Username and password are required'}, 400

        user = User.query.filter_by(username=username).first()
        if not user or not user.verify_password(password):
            return {'error': 'Invalid credentials'}, 401

        # Removed access_token and refresh_token generation
        return {
            'message': 'Login successful',
            'user_id': user.id,
            'user_role': user.role,
            'username': user.username
        }, 200

# Removed JWT-specific endpoints
# @auth_ns.route('/refresh')
# class RefreshToken(Resource):
#     # ... (removed content)

# @auth_ns.route('/protected')
# class Protected(Resource):
#     # ... (removed content)

# @auth_ns.route('/admin')
# class AdminProtected(Resource):
#     # ... (removed content)

# @auth_ns.route('/doctor')
# class DoctorProtected(Resource):
#     # ... (removed content)

# @auth_ns.route('/patient')
# class PatientProtected(Resource):
#     # ... (removed content)

# @auth_ns.route('/department_manager')
# class DepartmentManagerProtected(Resource):
#     # ... (removed content)


@auth_ns.route('/test')
class TestResource(Resource):
    def get(self):
        """Test endpoint for Flasgger (still accessible)"""
        return {"message": "Flasgger Test Successful!"}, 200