# config.py
import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hospital.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "your_strong_secret_key") # IMPORTANT: Change this in production
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-jwt-key") # IMPORTANT: Change this in production
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)