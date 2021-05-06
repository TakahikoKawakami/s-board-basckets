from app.config import templates
from app.common.managers import SessionManager
from logging import getLogger
import json


logger = getLogger(__name__)


def index(req, resp):
    logger.debug('access')

    if ('contract_id' in req.session):
        logger.debug('go to index')
        resp.redirect('/baskets', set_text=True, status_code=303)
        return
    else:
        logger.debug('go to welcome')
        resp.html = templates.render("home/welcome.pug")


def favicon():
    return app.send_static_file("favicon.ico")
