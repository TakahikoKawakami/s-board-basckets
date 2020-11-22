import os
from os.path import join, dirname
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


"""original"""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

   
class AppConfig(object):
    """base config"""

    ENV_DIVISION = os.environ.get("ENV_DIVISION")
    
    SMAREGI_CLIENT_ID = os.environ.get('SMAREGI_CLIENT_ID')
    SMAREGI_CLIENT_SECRET = os.environ.get('SMAREGI_CLIENT_SECRET')
    
    SECRET_KEY = os.environ.get('SECRET_KEY')

    """for flask"""
    DEBUG = False
    TESTING = False
    JSON_AS_ASCII = False
    JSON_SORT_KEYS = False

    APP_URI = os.environ.get('APP_URI')

    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_NATIVE_UNICODE = 'utf-8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DATABASE_NAME = os.environ.get('DB_NAME')
    DATABASE_FILE = os.path.join(BASE_DIR, DATABASE_NAME)
    DATABASE_ENGINE = None
    DATABASE_URI = None
    SQLALCHEMY_DATABASE_URI = None
        
    ENV_DIVISION_LOCAL = 'LOCAL'
    ENV_DIVISION_STAGING = 'STAGING'
    ENV_DIVISION_PRODUCTION = 'PROD'
    
    if (ENV_DIVISION == ENV_DIVISION_PRODUCTION):
        DEBUG = False
        TESTING = False
    elif (ENV_DIVISION == ENV_DIVISION_STAGING):        
        DEBUG = False
        TESTING = True
    elif (ENV_DIVISION == ENV_DIVISION_LOCAL):
        DEBUG = True
        TESTING = True
    
        DATABASE_NAME = os.environ.get('DB_NAME')
        DATABASE_FILE = os.path.join(BASE_DIR, DATABASE_NAME)
        DATABASE_ENGINE = create_engine('sqlite:///' + DATABASE_FILE, convert_unicode=True)
        DATABASE_URI = 'sqlite:///' + DATABASE_NAME
        SQLALCHEMY_DATABASE_URI = DATABASE_URI
