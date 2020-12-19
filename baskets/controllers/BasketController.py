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
from lib.Smaregi.API.POS.StoresApi import StoresApi

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

route = Blueprint('baskets', __name__, url_prefix='/baskets')

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
    apiConfig.accessToken = session['access_token']
    apiConfig.contractId = session['contract_id']


@route.route('/index', methods=['GET'])
def index():
    storesApi = StoresApi(apiConfig)
    storeList = storesApi.getStoreList()
    logger.info(storeList)
    return render_template('baskets/index.pug',stores=storeList)


@route.route('/summary', methods=['GET'])
def summary():
    # 分析期間を取得
    # 分析期間に該当する取引をDBから取得
    # ループでまわし、分析用データを作成する
    # DBにない日付の場合、該当日付の取引をAPIで取得、DBに保存
    # 対象取引データを取得
    transactionsApi = TransactionsApi(apiConfig)
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
    return render_template("baskets/summary.pug",
        nodes = result['nodes'],
        edges = result['edges'],
        ranking = ranking
    )
    

