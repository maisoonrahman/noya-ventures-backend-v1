import os

class Config:
    DEBUG = True

    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'instance', 'uploads')
