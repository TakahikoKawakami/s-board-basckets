import responder
from app.config import AppConfig

from app.controllers import AuthController, BasketController
from app.webhook import WebhookRouter
from app import database

import datetime
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


# staticをjinja2で解決するためにstaticフィルタを定義
def static_filter(path):
    return 'static/' + path + '?v=' + datetime.datetime.today().strftime('%y%m%d%H%M%S%F')
# staticをフィルタに追加
# v1系ではjinja_envだったが、v2からからtemplates._envに変更された
api.templates._env.filters.update(
    css=static_filter
)
add_routers(api)


@api.route('/webhook')
async def webhook(req, resp):
    @api.background.task
    def receivedWebhook(_header, _body):
        WebhookRouter.recieved(_header, _body)
    _header = req.headers
    _body = await req.media()
    receivedWebhook(_header, _body)
    resp.status_code = 200

