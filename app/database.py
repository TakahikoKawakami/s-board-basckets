from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


from app.config import AppConfig

config = AppConfig()

Base = declarative_base()
session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=config.DATABASE_ENGINE
    ))
# session = Session()