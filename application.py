import datetime
from flask import Flask,\
                  Blueprint
import logging
import logging.handlers
import pypugjs

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import AppConfig
from database import Database
from logging.config import dictConfig

# TODO: dictConfig、sessionからcontractId取得時に、format内にcontractIdを埋め込むこと
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
        'application': {
        'format': '[%(asctime)s][%(levelname)s] in %(module)s::%(funcName)s: %(message)s',
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'application': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'application',
            'filename': './log/test.log',
            'backupCount': 3,
            'when': 'D',
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi', 'application']
    }
})

app = Flask(__name__)

config = AppConfig()

app.secret_key = config.SECRET_KEY
app.config.from_object(config)

app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

db = SQLAlchemy(app)

def setRoute(routeArray):
    for route in routeArray:
        app.register_blueprint(route)
    return app


@app.context_processor
def add_staticfile():
    def staticfile_cp(fname):
        path = '/static/css/' + fname + '?v=' + datetime.datetime.today().strftime('%y%m%d%H%M%S%F')
        return path
    return dict(staticfile=staticfile_cp)

    
class Application():
    app = Flask(__name__)
    ENV_DIVISION_LOCAL = 'LOCAL'
    ENV_DIVISION_STAGING = 'STAGING'
    ENV_DIVISION_PRODUCTION = 'PROD'
    config = ''
    
    def __init__(self):
        self.config = AppConfig()
        self.app.secret_key = self.config.SECRET_KEY
        self.app.config.from_object(self.config)
        self.app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
        
        self.setDatabase()
        self.setManager()
        
        
    def setDatabase(self):
        self.db = Database(self)

        
    def setManager(self):
        self.migrate = Migrate(self.app, self.db, compare_type=True)
        self.manager = Manager(self.app)
        self.manager.add_command('db', MigrateCommand)
        self.manager.add_command('runserver', Server(host='localhost', port='8080'))
        return self.manager


    def setRoute(self, routeArray):
        for route in routeArray:
            self.app.register_blueprint(route)
        return self.app
        

    @app.context_processor
    def add_staticfile():
        def staticfile_cp(fname):
            path = '/static/css/' + fname + '?v=' + datetime.datetime.today().strftime('%y%m%d%H%M%S%F')
            return path
        return dict(staticfile=staticfile_cp)

