# config.py

import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-here'

    # SQLite database configuration
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        f"sqlite:///{os.path.join(basedir, 'peiris_grand_resort.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT token expiration (in seconds)
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours
