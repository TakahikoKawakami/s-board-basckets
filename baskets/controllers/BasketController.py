from flask import Blueprint, \
                  render_template,\
                  url_for,\
                  request,\
                  redirect,\
                  session,\
                  jsonify

import logging
import json
import datetime

from lib.Smaregi.config import config as SmaregiConfig
from lib.Smaregi.API.POS.TransactionsApi import TransactionsApi

from config import AppConfig
from factories.ModelFactory import ModelFactory
from baskets.models.Baskets import Basket


appConfig = AppConfig()
modelFactory = ModelFactory(appConfig)

apiConfig = SmaregiConfig(
    appConfig.ENV_DIVISION,
    appConfig.SMAREGI_CLIENT_ID,
    appConfig.SMAREGI_CLIENT_SECRET
)
transactionsApi = TransactionsApi(apiConfig)

route = Blueprint('basckets', __name__, url_prefix='/baskets')

logger = logging.getLogger('flask.app')


@route.before_request
def beforeRequest():
    if not ('access_token' in session):
        return redirect(url_for('accounts.getToken') + '?next=' + request.url)
    if not ('contract_id' in session):
        return redirect('/')
    if ('access_token_expires_in' in session):
        accessTokenExpiresIn = session['access_token_expires_in']
        now = datetime.datetime.now()
        if (accessTokenExpiresIn < now):
            return redirect(url_for('accounts.getToken') + '?next=' + request.url)
    transactionsApi.config.accessToken = session['access_token']
    transactionsApi.config.contractId = session['contract_id']


@route.route('/summary', methods=['GET'])
def summary():
    # 対象取引データを取得
    targetTransactionHeadList = transactionsApi.getTransaction()
    basket = modelFactory.createBasket()

    logger.info(targetTransactionHeadList)
    for transactionHead in targetTransactionHeadList:
        transactionDetailList = transactionsApi.\
            getTransactionDetail(transactionHead['transactionHeadId'])
        basket.append(transactionDetailList)

    result = basket.analyze(rate=10).result
    ranking = basket.salesRanking(top=3)
    basket.relationRanking("8000002")
    
#    rules = pyfpgrowth.generate_association_rules(patterns, 0.7)    
    return render_template("basckets/index.pug",
        nodes = result['nodes'],
        edges = result['edges'],
        ranking = ranking
    )
    

