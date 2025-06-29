# config.py
import os
# Removed: from datetime import timedelta # No longer needed if JWT_ACCESS_TOKEN_EXPIRES and JWT_REFRESH_TOKEN_EXPIRES are gone

class Config:
    # Database Configuration
    # SQLALCHEMY_DATABASE_URI specifies the database connection string.
    # 'sqlite:///hospital.db' indicates a SQLite database named hospital.db in the project root.
    # For production, consider using PostgreSQL or MySQL and setting this via environment variables.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hospital.db'

    # Disables a feature that tracks changes to objects and emits signals.
    # Setting it to False saves memory and avoids warnings for most applications.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security
    # SECRET_KEY is used for cryptographic operations in Flask, such as session management.
    # It's crucial to set a strong, unique value and manage it securely (e.g., via environment variables) in production.
    SECRET_KEY = os.getenv("SECRET_KEY", "your_strong_secret_key")  # IMPORTANT: Change in production

    # Removed JWT Configuration
    # JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-jwt-key")
    # JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    # JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)