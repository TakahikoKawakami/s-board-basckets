from tortoise import Tortoise, run_async

async def migrate():
   # connect DB
    await Tortoise.init(
        db_url="sqlite://db.sqlite3",  # DB URL
        modules={"models": ["models"]}  # Modelを書いたファイルを指定
    )

    # run migrate
    await Tortoise.generate_schemas()

run_async(migrate())