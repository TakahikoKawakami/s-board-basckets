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

db_url = config.DATABASE_CONNECTION + "://" + \
    config.DATABASE_USERNAME + ":" + config.DATABASE_PASSWORD + \
    "@" + config.DATABASE_HOST + ":" + config.DATABASE_PORT + "/" + config.DATABASE_NAME


TORTOISE_ORM = {
    "connections": {"default":db_url},
    "apps": {
        "models": {
            "models": [
                "app.models",
                "aerich.models" # 最後に必要
            ],
            "default_connection": "default",
        },
    },
}


async def init():
    await Tortoise.init(
        # {DB_TYPE}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}?{PARAM1}=values&{PARAM2}=values
        db_url = config.DATABASE_CONNECTION + "://" + \
            config.DATABASE_USERNAME + ":" + config.DATABASE_PASSWORD + \
            "@" + config.DATABASE_HOST + ":" + config.DATABASE_PORT + "/" + config.DATABASE_NAME,
        # db_url = "mysql://preview:preview@mysql:3306/local",
        # db_url=config.DATABASE_URI,  # DB URL
        modules={"models": [
            "app.models.Accounts"
        ]}  # Modelを書いたファイルを指定
    )

async def close():
    await Tortoise.close_connections()