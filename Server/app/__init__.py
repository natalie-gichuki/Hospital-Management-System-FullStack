from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restx import Api  

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
api = Api(  # ✅ instantiate Flask-RESTX Api here
    title="Hospital Management System API",
    version="1.0",
    description="API documentation for the Hospital Management System.",
    doc="/docs"  # Swagger UI available at /docs
)

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    api.init_app(app)

    # === RESTX Namespaces ===
    from app.routes.patients import patient_ns
    from app.routes.doctors import doctor_ns
    from app.routes.departments import department_ns
    from app.routes.appointments import appointments_ns
    from app.routes.medical_records import medical_ns
    from app.routes.auth import auth_ns

    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(patient_ns, path="/patients")
    api.add_namespace(doctor_ns, path="/doctors")
    api.add_namespace(department_ns, path="/departments")
    api.add_namespace(appointments_ns, path="/appointments")
    api.add_namespace(medical_ns, path="/medical-records")

    with app.app_context():
        from . import models
        # db.create_all()  # Flask-Migrate handles this
    return app
