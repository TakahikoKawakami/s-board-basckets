from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os

db = SQLAlchemy()

# config = app.config
# app = app.app
# db.init_app(app)
# db.app = app
# db_session = scoped_session(sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=config.DATABASE_ENGINE
#     ))
# Base = declarative_base()
# Base.query = db_session.query_property()

# def init_db():
#     # Base.metadatacreate_all(bind=config.DATABASE_ENGINE)
#     Base.create_all(bind=config.DATABASE_ENGINE)



 
class Database():
    db = SQLAlchemy()

    def __init__(self, app):
        self.config = app.config
        self.app = app.app
        self.db.init_app(self.app)
        self.db.app = self.app
        self.db_session = scoped_session(sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.config.DATABASE_ENGINE
            ))
        self.Base = declarative_base()
        self.Base.query = self.db_session.query_property()
        
    def init_db(self):
        # self.Base.metadatacreate_all(bind=self.config.DATABASE_ENGINE)
        self.Base.create_all(bind=self.config.DATABASE_ENGINE)
