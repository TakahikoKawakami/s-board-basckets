import responder

from app.config import AppConfig
from app import database
from app.router import add_routers

api = responder.API(
    secret_key=AppConfig.SECRET_KEY,
    templates_dir="app/templates",
    static_dir="app/static"
)

# 立ち上げのタイミングでDBへのコネクションを確立
@api.on_event("startup")
async def start_db_connection():
    await database.init()

# 落とすタイミングでDBコネクションを切断
@api.on_event("shutdown")
async def close_db_connection():
    await database.close()

add_routers(api)
