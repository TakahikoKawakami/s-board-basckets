from tortoise import Tortoise

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

db_url = "{}://{}:{}@{}:{}/{}".format(
    config.DATABASE_CONNECTION,
    config.DATABASE_USERNAME,
    config.DATABASE_PASSWORD,
    config.DATABASE_HOST,
    config.DATABASE_PORT,
    config.DATABASE_NAME
)

TORTOISE_ORM = {
    "connections": {"default":db_url},
    "apps": {
        "models": { # app名. relationのrelated_nameでは、{この名称}.{modelクラス名}
            "models": [
                "app.models",
                "aerich.models" # 最後に必要
            ],
            "default_connection": "default",
        },
    },
    'use_tz': False,
    'timezone': 'Asia/Tokyo',
}

async def init():
    await Tortoise.init(TORTOISE_ORM)
    Tortoise.init_models(['app.models'], 'models') # necessary for relations

async def close():
    await Tortoise.close_connections()