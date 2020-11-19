from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os

import settings


db = SQLAlchemy()

db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=settings.DATABASE_ENGINE
    ))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadatacreate_all(bind=settings.DATABASE_ENGINE)
    

