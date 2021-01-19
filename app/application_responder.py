import responder
from app.config import AppConfig

from app.controllers import AuthController, BasketController

import datetime
# from router import add_routers

api = responder.API(secret_key=AppConfig.SECRET_KEY)

# staticをjinja2で解決するためにstaticフィルタを定義
def static_filter(path):
    return '/static/' + path + '?v=' + datetime.datetime.today().strftime('%y%m%d%H%M%S%F')
# staticをフィルタに追加
# v1系ではjinja_envだったが、v2からからtemplates._envに変更された
api.templates._env.filters.update(
    css=static_filter
)
# api.add_route('/baskets/associate', BasketController.BeforeRequest, before_request=True)
api.add_route('/accounts/login', AuthController.login)
api.add_route('/accounts/logout', AuthController.logout)
api.add_route('/accounts/authorize', AuthController.authorize)
api.add_route('/baskets/associate', BasketController.Associate)
api.templates._env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')
# add_routers(api)
