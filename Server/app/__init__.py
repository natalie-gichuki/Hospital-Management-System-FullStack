from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restx import Api
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

api = Api(
    title="Hospital Management System API",
    version="1.0",
    description="API documentation for the Hospital Management System.",
    doc="/docs"
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
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
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(patient_ns, path="/patients")
    api.add_namespace(doctor_ns, path="/doctors")
    api.add_namespace(department_ns, path="/departments")
    api.add_namespace(appointments_ns, path="/appointments")
    api.add_namespace(medical_ns, path="/medical-records")

    with app.app_context():
        from . import models
        db.create_all()  # Uncomment this line if you want Flask-SQLAlchemy to create tables
                          # on app startup. However, it's generally recommended to use Flask-Migrate
                          # for schema management in production environments (flask db migrate/upgrade).

    return app