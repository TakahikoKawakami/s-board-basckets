import responder
from app.controllers import AuthController, HomeController


def add_routers(api: responder.API):
    api.add_route("/accounts/authorize", AuthController.authorize)
    api.add_route("/accounts/token", AuthController.getToken)
    api.add_route("/", HomeController.index)


def favicon():
    return app.send_static_file("favicon.ico")