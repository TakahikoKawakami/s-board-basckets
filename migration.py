from tortoise import Tortoise, run_async
from app.database import init
from app.config import AppConfig

config = AppConfig()



async def migrate():
    # connect DB
    await init()

    # run migrate
    await Tortoise.generate_schemas()

run_async(migrate())