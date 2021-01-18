from application_responder import api
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
        return redirect(url_for('baskets.index'))
        return render_template(
            "home/index.pug",
            contractId = resp.session['contract_id'],
            message = ''
        )
    else:
        logger.debug('go to welcome')
        resp.html = api.template("home/welcome.pug")


@api.route('/favicon.ico')
def favicon():
    return app.send_static_file("favicon.ico")