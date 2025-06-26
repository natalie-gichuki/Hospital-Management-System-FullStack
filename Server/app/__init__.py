# app/__init__.py
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager # Import JWTManager

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager() # Initialize JWTManager

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app) # Initialize JWT with the app
    api = Api(app)

    # Import and add the authentication routes
    from app.routes.auth import Register, Login, RefreshToken, Protected # Add Protected for example
    api.add_resource(Register, '/auth/register')
    api.add_resource(Login, '/auth/login')
    api.add_resource(RefreshToken, '/auth/refresh')
    api.add_resource(Protected, '/auth/protected') # Example protected route

    # Import and add Department routes (already existing)
    from app.routes.departments import DepartmentList, DepartmentByID
    api.add_resource(DepartmentList, '/departments')
    api.add_resource(DepartmentByID, '/departments/<int:id>')

    # Import and add the new API routes
    from app.routes.doctors import DoctorList, DoctorByID
    api.add_resource(DoctorList, '/doctors')
    api.add_resource(DoctorByID, '/doctors/<int:id>')

    from app.routes.patients import PatientList, PatientByID
    api.add_resource(PatientList, '/patients')
    api.add_resource(PatientByID, '/patients/<int:id>')

    from app.routes.appointments import AppointmentList, AppointmentByID
    api.add_resource(AppointmentList, '/appointments')
    api.add_resource(AppointmentByID, '/appointments/<int:id>')

    from app.routes.medical_records import MedicalRecordList, MedicalRecordByID
    api.add_resource(MedicalRecordList, '/medical_records')
    api.add_resource(MedicalRecordByID, '/medical_records/<int:id>')

    with app.app_context():
        from . import models # Ensure models are loaded for SQLAlchemy
        db.create_all() # This creates tables if they don't exist based on models

    return app