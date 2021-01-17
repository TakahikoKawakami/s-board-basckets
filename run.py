import responder
import uvicorn
import json
import route

import logging

from application import app as flask_app
from app.controllers import HomeController
from webhook import WebhookRouter


api = responder.API()

api.mount("/", flask_app)
api.logger = logging.getLogger('flask.app')

# api.add_route('/webhook', HomeController.index)
@api.route('/webhook')
async def webhook(req, resp):
    @api.background.task
    def receivedWebhook(data):
        WebhookRouter.recieve(data)
    data = await req.media()
    receivedWebhook(data)
    resp.status_code = 200


"""Webサーバを立ち上げる際に実行するファイル"""
if __name__ == "__main__":
    # api.run(address="0.0.0.0", port=5500, debug=True)
    # uvicorn.run("run:api", host='0.0.0.0', log_config="logging_config.json", port=5500, debug=True, reload=True)
    uvicorn.run("run:api", host='0.0.0.0', port=5500, debug=True, reload=True)
