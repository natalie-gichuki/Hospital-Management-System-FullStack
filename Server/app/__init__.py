# app/__init__.py (Updated)
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flasgger import Swagger # <--- NEW IMPORT

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
api = Api() # Moved api instantiation here for clarity

# Define Swagger template (basic information about your API)
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Hospital Management System API",
        "description": "API documentation for the Hospital Management System.",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
            "BearerAuth": []
        }
    ],
    "schemes": [
        "http", # Use http for development, change to https for production
        "https"
    ],
    "consumes": [
        "application/json"
    ],
    "produces": [
        "application/json"
    ]
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/" # This is the URL where you'll access the documentation
}


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    api.init_app(app) # Initialize api with the app

    # Initialize Flasgger
    Swagger(app, template=swagger_template, config=swagger_config) # <--- NEW LINE

    # Import and add the authentication routes
    from app.routes.auth import Register, Login, RefreshToken, Protected, AdminProtected, DoctorProtected, PatientProtected, DepartmentManagerProtected
    api.add_resource(Register, '/auth/register')
    api.add_resource(Login, '/auth/login')
    api.add_resource(RefreshToken, '/auth/refresh')
    api.add_resource(Protected, '/auth/protected')
    api.add_resource(AdminProtected, '/auth/admin-protected') # Renamed for clarity
    api.add_resource(DoctorProtected, '/auth/doctor-protected')
    api.add_resource(PatientProtected, '/auth/patient-protected')
    api.add_resource(DepartmentManagerProtected, '/auth/department-manager-protected')


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
        from . import models
        # db.create_all() # Comment this out if using Flask-Migrate, as 'flask db upgrade' handles table creation

    return app