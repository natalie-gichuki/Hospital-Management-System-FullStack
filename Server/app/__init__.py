from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('app.config.Config')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import models
        from .routes import appointments, departments, doctors, patients, medical_records

        # Register blueprints
        app.register_blueprint(doctors.doctor_bp)
        app.register_blueprint(patients.patient_bp)
        app.register_blueprint(appointments.appointment_bp)
        #app.register_blueprint(departments.department_bp)
        #app.register_blueprint(medical_records.record_bp)

        db.create_all()

    return app
