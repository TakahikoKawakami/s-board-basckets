from app.application_responder import api
from app.common.managers import SessionManager
from logging import getLogger
import json


logger = getLogger(__name__)

@api.route(before_request=True)
def beforeRequest(req, resp):
    pass

@api.route('/')
def index(req, resp):
    logger.debug('access')

    if ('contract_id' in req.session):
        logger.debug('go to index')
        resp.redirect('/baskets/associate')
        return
    else:
        logger.debug('go to welcome')
        resp.html = api.template("home/welcome.pug")


@api.route('/favicon.ico')
def favicon():
    return app.send_static_file("favicon.ico")