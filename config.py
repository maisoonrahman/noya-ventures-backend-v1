import os 

class Config:
    DEBUG = True
    DB_HOST = 'dev_db_host'
    DB_USER = 'dev_db_user'
    DB_PASSWORD = 'dev_db_pass'
    DB_NAME = 'noya_vc_dev'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'instance', 'uploads')