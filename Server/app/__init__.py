from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Api, Resource


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app,db)
    api = Api(app)

    from .routes.patients import HomeResource, Patient_List, Patient_By_ID, PatientMedicalRecords
    from .routes.medical_records import MedicalRecords, MedicalRecordByID


    # ✅ Add resources here
    api.add_resource(HomeResource, '/')
    api.add_resource(Patient_List, '/patients')
    api.add_resource(Patient_By_ID, '/patients/<int:id>')
    api.add_resource(PatientMedicalRecords, '/patients/<int:id>/records')
    api.add_resource(MedicalRecords, '/records')
    api.add_resource(MedicalRecordByID, '/records/<int:id>')


    with app.app_context():
        from . import models
        from .routes import appointments, departments, doctors, patients, medical_records
        db.create_all()

        # 

    return app