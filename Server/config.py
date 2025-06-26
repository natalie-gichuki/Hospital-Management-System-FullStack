import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hospital.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")

# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# migrations/env.py
