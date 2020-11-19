# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ENV_DIVISION = os.environ.get("ENV_DIVISION")

APP_URI = os.environ.get('APP_URI')

SMAREGI_CLIENT_ID = os.environ.get('SMAREGI_CLIENT_ID')
SMAREGI_CLIENT_SECRET = os.environ.get('SMAREGI_CLIENT_SECRET')

SECRET_KEY = os.environ.get('SECRET_KEY')

if (ENV_DIVISION == 'LOCAL'):
    DATABASE_NAME = os.environ.get('DB_NAME')
    DATABASE_FILE = os.path.join(BASE_DIR, DATABASE_NAME)
    DATABASE_ENGINE = create_engine('sqlite:///' + DATABASE_FILE, convert_unicode=True)
    DATABASE_URI = 'sqlite:///' + DATABASE_NAME
