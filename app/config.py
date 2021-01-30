import responder
import os
import datetime
from os.path import join, dirname
from pathlib import Path
from dotenv import load_dotenv

# background
backgroundQueue = responder.background.BackgroundQueue()

# template
templates = responder.templates.Templates(
    directory="app/templates"
)
# staticをjinja2で解決するためにstaticフィルタを定義
def static_filter(path):
    # directoryで指定したtemplatesと同階層ががroot扱い？
    return '/static/' + path + '?v=' + datetime.datetime.today().strftime('%y%m%d%H%M%S%F')
# staticをフィルタに追加
# v1系ではjinja_envだったが、v2からからtemplates._envに変更された
templates._env.filters.update(
    css=static_filter
)
templates._env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

"""original"""
BASE_DIR2 = os.path.dirname(os.path.abspath(__file__))
APP_DIR = Path(__file__)
BASE_DIR = APP_DIR.parent.parent
dotenv_path = join(str(BASE_DIR), '.env')
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
    DATABASE_FILE = BASE_DIR / DATABASE_NAME
    DATABASE_ENGINE = None
    DATABASE_URI = None
    SQLALCHEMY_DATABASE_URI = None

    ENV_DIVISION_MOCK = 'MOCK'
    ENV_DIVISION_LOCAL = 'LOCAL'
    ENV_DIVISION_STAGING = 'STAGING'
    ENV_DIVISION_PRODUCTION = 'PROD'
    
    DATABASE_CONNECTION = os.environ.get('DB_CONNECTION') # mysql, sqlite3, etc.
    DATABASE_USERNAME = os.environ.get('DB_USERNAME')
    DATABASE_PASSWORD = os.environ.get('DB_PASSWORD')
    DATABASE_HOST = os.environ.get('DB_HOST')
    DATABASE_PORT = os.environ.get('DB_PORT')
    DATABASE_NAME = os.environ.get('DB_NAME')

    if (ENV_DIVISION == ENV_DIVISION_PRODUCTION):
        DEBUG = False
        TESTING = False
    elif (ENV_DIVISION == ENV_DIVISION_STAGING):
        DEBUG = False
        TESTING = True
    elif (ENV_DIVISION == ENV_DIVISION_LOCAL or ENV_DIVISION == ENV_DIVISION_MOCK):
        DEBUG = True
        TESTING = True
    

