import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-here'
    
    # MySQL database configuration
    DB_SERVER = os.environ.get('DB_SERVER') or 'localhost:3306'
    DB_DATABASE = 'peiris_grand_resort'
    DB_USERNAME = os.environ.get('DB_USERNAME') or 'root'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or '8385'
    
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}"
        f"@{DB_SERVER}/{DB_DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours
