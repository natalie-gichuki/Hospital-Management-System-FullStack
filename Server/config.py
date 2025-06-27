# Imports Python’s built-in os module, which lets you access environment variables from your .env file or system.
import os

# This defines a configuration class that Flask (and extensions like Flask-SQLAlchemy) can use to configure your app.
class Config:
    # Reads the environment variable named DATABASE_URL from .env. (It tells SQLAlchemy where the database is and how to connect to it.)

    SQLALCHEMY_DATABASE_URI = 'sqlite:///hospital.db'

    # Disables a feature that tracks changes to objects and emits signals. (Setting it to False saves memory and avoids warnings )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Reads the SECRET_KEY from the .env file. (If it’s not set, it uses "fallback-secret" as a default backup (this is helpful for development).)
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
