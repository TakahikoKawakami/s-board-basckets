from flask import Blueprint, \
                  render_template,\
                  url_for,\
                  request,\
                  redirect,\
                  session

from logging import getLogger
import json


logger = getLogger('flask.app')

route =  Blueprint('home', __name__)

@route.before_request
def beforeRequest():
    pass        
    # transactionsApi.config.accessToken = session['access_token']
    # transactionsApi.config.contractId = session['contract_id']
#    if not ('contract_id' in session):
#        if ()
#    self.getToken()


@route.route('/')
def index():
    logger.debug('access')
    # account = Accounts.Account
    # accounts = account.query.order_by(account.id.asc())
    accounts = []
    logger.debug('go to index')
    return render_template(
        "books/index.html",
        accounts=accounts,
        message = ''
    )

    if ('contract_id' in session):
        account = Accounts.Account
        accounts = account.query.order_by(account.id.asc())
        logger.debug('go to index')
        return render_template(
            "books/index.html",
            accounts=accounts,
            message = ''
        )
    else:
        logger.debug('go to welcome')
        return render_template("home/welcome.pug")
