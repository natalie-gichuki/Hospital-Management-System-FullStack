from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.models import User, Doctor, Patient
from app import db, jwt
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    current_user
)
from sqlalchemy.exc import IntegrityError
from datetime import timedelta

auth_ns = Namespace('auth', description="Authentication and authorization operations")

# JWT user loader
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()

# Role decorator
def role_required(required_roles):
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            if not current_user:
                return {"msg": "User not found in token identity"}, 401
            if current_user.role not in required_roles:
                return {"msg": f"Access denied: Requires one of {', '.join(required_roles)}"}, 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

# Models for Swagger
register_model = auth_ns.model('Register', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'role': fields.String(default='patient', enum=['admin', 'doctor', 'patient', 'department_manager']),
    'doctor_id': fields.Integer(required=False),
    'patient_id': fields.Integer(required=False)
})

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

token_response = auth_ns.model('TokenResponse', {
    'access_token': fields.String(),
    'refresh_token': fields.String(),
    'user_role': fields.String(),
    'user_id': fields.Integer()
})


@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model)
    @auth_ns.response(201, 'User registered successfully')
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
            new_user.password = password
            db.session.add(new_user)
            db.session.commit()

            # Link to Doctor/Patient profile if provided
            if role == 'doctor' and data.get('doctor_id'):
                doctor = Doctor.query.get(data['doctor_id'])
                if doctor:
                    doctor.user_id = new_user.id
                    db.session.commit()
            elif role == 'patient' and data.get('patient_id'):
                patient = Patient.query.get(data['patient_id'])
                if patient:
                    patient.user_id = new_user.id
                    db.session.commit()

            return {'message': 'User registered successfully', 'user_id': new_user.id, 'role': new_user.role}, 201

        except IntegrityError:
            db.session.rollback()
            return {'error': 'Username already exists or invalid data'}, 409
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    @auth_ns.marshal_with(token_response)
    @auth_ns.response(200, 'Login successful')
    @auth_ns.response(401, 'Invalid credentials')
    def post(self):
        """Login and get tokens"""
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


@auth_ns.route('/refresh')
class RefreshToken(Resource):
    @jwt_required(refresh=True)
    @auth_ns.response(200, 'New access token generated')
    @auth_ns.response(401, 'Invalid refresh token')
    def post(self):
        """Refresh access token using refresh token"""
        current_user_id = get_jwt_identity()
        new_token = create_access_token(identity=current_user_id)
        return {'access_token': new_token}, 200


@auth_ns.route('/protected')
class Protected(Resource):
    @jwt_required()
    @auth_ns.response(200, 'Authenticated')
    @auth_ns.response(401, 'Unauthorized')
    def get(self):
        """Accessible by any logged-in user"""
        user = User.query.get(get_jwt_identity())
        if not user:
            return {"msg": "User not found"}, 404
        return {"msg": f"Hello, {user.username}! You are authenticated as {user.role}"}, 200


@auth_ns.route('/admin')
class AdminProtected(Resource):
    @role_required(['admin'])
    def get(self):
        """Admin-only endpoint"""
        return {"msg": f"Welcome Admin, {current_user.username}!"}, 200


@auth_ns.route('/doctor')
class DoctorProtected(Resource):
    @role_required(['doctor', 'admin'])
    def get(self):
        """Doctor-only endpoint"""
        return {"msg": f"Welcome Dr. {current_user.username}!"}, 200


@auth_ns.route('/patient')
class PatientProtected(Resource):
    @role_required(['patient', 'admin'])
    def get(self):
        """Patient-only endpoint"""
        return {"msg": f"Welcome Patient {current_user.username}!"}, 200


@auth_ns.route('/department_manager')
class DepartmentManagerProtected(Resource):
    @role_required(['department_manager', 'admin'])
    def get(self):
        """Department Manager endpoint"""
        return {"msg": f"Welcome Department Manager {current_user.username}!"}, 200


@auth_ns.route('/test')
class TestResource(Resource):
    def get(self):
        """Test endpoint for Flasgger"""
        return {"message": "Flasgger Test Successful!"}, 200
