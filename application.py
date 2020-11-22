from flask import Flask,\
                  Blueprint
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from config import AppConfig

from database import Database

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

