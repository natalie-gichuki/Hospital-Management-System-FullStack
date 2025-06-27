from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from flask_restful import Api, Resource



db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.url_map.strict_slashes = False


    app.config.from_object('app.config.Config')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)

    migrate.init_app(app,db)
    api = Api(app)


    from .routes.patients import HomeResource, Patient_List, Patient_By_ID, PatientMedicalRecords
    from .routes.medical_records import MedicalRecords, MedicalRecordByID


    # ✅ Add resources here
    api.add_resource(HomeResource, '/')
    api.add_resource(Patient_List, '/patients/')
    api.add_resource(Patient_By_ID, '/patients/<int:id>')
    api.add_resource(PatientMedicalRecords, '/patients/<int:id>/records')
    api.add_resource(MedicalRecords, '/records/')
    api.add_resource(MedicalRecordByID, '/records/<int:id>')




    with app.app_context():
        from . import models
        from .routes import appointments, departments, doctors, patients, medical_records

        # Register blueprints
        app.register_blueprint(doctors.doctor_bp)
        
        app.register_blueprint(appointments.appointment_bp)
        #app.register_blueprint(departments.department_bp)
        #app.register_blueprint(medical_records.record_bp)

        db.create_all()
          #


    return app
