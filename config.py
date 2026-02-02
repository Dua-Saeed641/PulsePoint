import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Config:
    # Secret key is used by Flask to protect session data and forms
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key')

    # Database URI (can come from .env or fallback to local SQLite)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///hospital.db')

    # Disable modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_CREATE_EMAIL = os.getenv('ADMIN_CREATE_EMAIL', 'duasaeed641@gmail.com')
    ADMIN_CREATE_PASSWORD = os.getenv('ADMIN_CREATE_PASSWORD', 'duasaeed')
