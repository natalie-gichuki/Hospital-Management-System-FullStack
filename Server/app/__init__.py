# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
# Removed: from flask_jwt_extended import JWTManager # <--- REMOVED THIS IMPORT
from flask_restx import Api
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
# Removed: jwt = JWTManager() # <--- REMOVED THIS LINE

api = Api(
    title="Hospital Management System API",
    version="1.0",
    description="API documentation for the Hospital Management System.",
    doc="/docs"
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Keeping CORS as it's good practice for frontend-backend interaction
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}})

    db.init_app(app)
    migrate.init_app(app, db)
    # Removed: jwt.init_app(app) # <--- REMOVED THIS LINE
    api.init_app(app)

    # === RESTX Namespaces ===
    # Import namespaces, assuming these are flask_restx.Namespace objects
    from app.routes.auth import auth_ns
    from app.routes.patients import patient_ns
    from app.routes.doctors import doctor_ns
    from app.routes.departments import department_ns
    from app.routes.appointments import appointments_ns
    from app.routes.medical_records import medical_ns

    # Register namespaces with the API
    # I've kept the trailing slashes here for consistency with your frontend calls
    api.add_namespace(auth_ns, path="/auth/")
    api.add_namespace(patient_ns, path="/patients/")
    api.add_namespace(doctor_ns, path="/doctors/")
    api.add_namespace(department_ns, path="/departments/")
    api.add_namespace(appointments_ns, path="/appointments/")
    api.add_namespace(medical_ns, path="/medical-records/")

    with app.app_context():
        from . import models
        db.create_all()

    return app