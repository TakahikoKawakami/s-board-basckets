from flask import Blueprint, \
                  render_template,\
                  url_for,\
                  request,\
                  redirect,\
                  session

import logging
import json
import datetime

from lib.Smaregi.config import config as SmaregiConfig
from lib.Smaregi.API.POS.TransactionsApi import TransactionsApi

from config import AppConfig
from baskets.models.Baskets import Basket

appConfig = AppConfig()
apiConfig = SmaregiConfig(
    appConfig.ENV_DIVISION,
    appConfig.SMAREGI_CLIENT_ID,
    appConfig.SMAREGI_CLIENT_SECRET
)
transactionsApi = TransactionsApi(apiConfig)

route = Blueprint('basckets', __name__, url_prefix='/basckets')


@route.before_request
def beforeRequest():
    transactionsApi.config.accessToken = session['access_token']
    transactionsApi.config.contractId = session['contract_id']
#    if not ('contract_id' in session):
#        if ()
#    self.getToken()


@route.route('/transactions', methods=['GET'])
def getTransaction():
    targetTransactionHeadList = transactionsApi.getTransaction()
    basket = Basket()

    for transactionHead in targetTransactionHeadList:
        transactionDetailList = transactionsApi.\
            getTransactionDetail(transactionHead['transactionHeadId'])
        basket.append(transactionDetailList)

    result = basket.analyze().result
    
#    rules = pyfpgrowth.generate_association_rules(patterns, 0.7)    
    print ('nodes')
    print (result['nodes'])
    print ('edges')
    print (result['edges'])
    return render_template("basckets/index.html",
#        message = json.dumps(basket, indent=4),
        message = basket.salesRanking(),
        nodes = result['nodes'],
        edges = result['edges']
    )
    

