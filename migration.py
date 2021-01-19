from tortoise import Tortoise, run_async
from app.config import AppConfig

config = AppConfig()
async def migrate():
    print(config.DATABASE_URI)
    # connect DB
    await Tortoise.init(
        db_url=config.DATABASE_URI,  # DB URL
        modules={"models": ["models"]}  # Modelを書いたファイルを指定
    )

    # run migrate
    await Tortoise.generate_schemas()

run_async(migrate())