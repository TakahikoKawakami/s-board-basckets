import responder
import app.controllers.api as ApiControllers
import app.controllers as Controllers
# from app.controllers.view import *


def add_routers(api: responder.API):
    # api.add_route("/accounts/token", AuthController.getToken)
    # api.add_route('/favicon.ico', HomeController.favicon)
    api.add_route(
        '/accounts/login',
        Controllers.AuthController.login
    )
    api.add_route(
        '/accounts/logout',
        Controllers.AuthController.logout
    )
    api.add_route(
        '/accounts/authorize',
        Controllers.AuthController.authorize
    )
    api.add_route(
        '/accounts/setting',
        Controllers.SettingController.AccountSetting
    )
    api.add_route(
        '/accounts/setting/stores',
        Controllers.SettingController.AccountStore
    )
    api.add_route(
        '/baskets',
        Controllers.BasketController.Basket
    )
    api.add_route(
        '/baskets/associate/result',
        Controllers.BasketController.AssociateResult
    )

    api.add_route(
        '/api/baskets',
        ApiControllers.ApiBasketController.ApiBasket
    )

    api.add_route(
        '/webhook',
        Controllers.WebhookController.Webhook
    )
    api.add_route(
        '/',
        Controllers.HomeController.index
    )
