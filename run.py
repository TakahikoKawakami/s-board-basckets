import uvicorn
import json

import logging

from app.application_responder import api
# from application import app as flask_app
from app.controllers import HomeController
from app.webhook import WebhookRouter

from tortoise import Tortoise


# 立ち上げのタイミングでDBへのコネクションを確立
# @api.on_event("startup")
# async def start_db_connection():
#     await Tortoise.init(
#         db_url="sqlite://db.sqlite3",
#         modules={"models": ["models"]}
#     )

# # 落とすタイミングでDBコネクションを切断
# @api.on_event("shutdown")
# async def close_db_connection():
#     await Tortoise.close_connections()

# router.pyにてルーティングを設定
# add_routers(api)

# api.mount("/", flask_app)
# api.logger = logging.getLogger('flask.app')

@api.route('/webhook')
async def webhook(req, resp):
    @api.background.task
    def receivedWebhook(_header, _body):
        WebhookRouter.recieved(_header, _body)
    _header = req.headers
    _body = await req.media()
    receivedWebhook(_header, _body)
    resp.status_code = 200


"""Webサーバを立ち上げる際に実行するファイル"""
if __name__ == "__main__":
    # api.run(address="0.0.0.0", port=5500, debug=True)
    # uvicorn.run("run:api", host='0.0.0.0', log_config="logging_config.json", port=5500, debug=True, reload=True)
    uvicorn.run(
        "app.application_responder:api", 
        host='0.0.0.0', 
        port=5500, 
        debug=True, 
        reload=True,
        reload_dirs=['app']
    )
