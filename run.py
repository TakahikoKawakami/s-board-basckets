import responder
import uvicorn
import json
import route

from application import app as flask_app
from app.controllers import HomeController


api = responder.API()

api.mount("/", flask_app)

# api.add_route('/webhook', HomeController.index)
@api.route('/webhook')
def hello(req, resp):
    print('hello')
    # resp.headers = {'Content-Type': 'application/json: charset=utf-8'}
    # resp.content = json.dumps({"hello": "world"},ensure_ascii=False )
    resp.text = "hello world"

"""Webサーバを立ち上げる際に実行するファイル"""
if __name__ == "__main__":
    uvicorn.run(api, host='0.0.0.0' ,port=5500)
