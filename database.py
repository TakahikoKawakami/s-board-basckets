from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


from config import AppConfig


Base = declarative_base()
Session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=AppConfig.DATABASE_ENGINE
    ))
session = Session()