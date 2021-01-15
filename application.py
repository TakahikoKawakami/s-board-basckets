import datetime
from flask import Flask,\
                  render_template,\
                  request,\
                  redirect,\
                  url_for,\
                  session,\
                  Blueprint
import logging
import logging.handlers
import pypugjs

import scheduler

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import AppConfig
from database import Database
from logging.config import dictConfig
from authorizations.controllers import AuthController
from baskets.controllers import BasketController
from home.controllers import HomeController

from webhook import route as WebhookRoute, TransactionsWebhook

# TODO: dictConfig、sessionからcontractId取得時に、format内にcontractIdを埋め込むこと
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s(%(lineno)d): %(message)s',
        },
        'application': {
        'format': '[%(asctime)s][%(levelname)-5s] in %(module)s::%(funcName)s(%(lineno)d): %(message)s', # 5s: 右寄せ -5s: 左寄せ
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
            'when': 'MIDNIGHT',
            'backupCount': 31,
            'encoding': 'utf-8'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi', 'application']
    },
    'disable_existing_loggers': False,
})

app = Flask(__name__)

config = AppConfig()

app.secret_key = config.SECRET_KEY
app.config.from_object(config)

app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

db = SQLAlchemy(app)

db.init_app(app)
db.app = app


@HomeController.route.route('/favicon.ico')
def favicon():
    return app.send_static_file("favicon.ico")
    

def setRoute(routeArray):
    for route in routeArray:
        app.register_blueprint(route)
    return app


setRoute([
    HomeController.route,
    AuthController.route,
    BasketController.route,
    WebhookRoute,
])


@app.context_processor
def add_staticfile():
    def staticfile_cp(fname):
        path = '/static/' + fname + '?v=' + datetime.datetime.today().strftime('%y%m%d%H%M%S%F')
        return path
    return dict(staticfile=staticfile_cp)

