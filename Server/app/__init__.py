from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app,db)

    from app.routes.departments import DepartmentList, DepartmentByID


    api.add_resource(DepartmentList, '/departments')
    api.add_resource(DepartmentByID, '/departments/<int:id>')

    with app.app_context():
        from . import models
        from .routes import appointments, departments, doctors, patients, medical_records
        db.create_all()

    return app