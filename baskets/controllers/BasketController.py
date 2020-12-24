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
from baskets.repositories.BasketAnalysesRepository import BasketAnalysesRepository
from common.DictionaryUtil import DictionaryUtil


logger = logging.getLogger('flask.app')
appConfig = AppConfig()
modelFactory = ModelFactory(appConfig)

apiConfig = SmaregiConfig(
    appConfig.ENV_DIVISION,
    appConfig.SMAREGI_CLIENT_ID,
    appConfig.SMAREGI_CLIENT_SECRET,
    logger
)

route = Blueprint('baskets', __name__, url_prefix='/baskets')



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
    targetStoreId = request.args.get('condition_store')
    targetDateFrom = request.args.get('condition_date_from')
    targetDateTo = request.args.get('condition_date_to')
    if  (targetStoreId is None) or\
        (targetDateFrom is None) or (targetDateFrom == "") or\
        (targetDateTo is None) or (targetDateTo == ""):
        return redirect(url_for('baskets.index'))

    logger.info("-----search condition-----")
    logger.info("storeId     : " + targetStoreId)
    logger.info("search_from : " + targetDateFrom)
    logger.info("search_to   : " + targetDateTo)

    # 分析期間の取引ヘッダを取得
    transactionsApi = TransactionsApi(apiConfig)
    targetTransactionHeadList = transactionsApi.getTransaction(
        whereDict={
            'store_id': targetStoreId,
            'sum_date-from': targetDateFrom,
            'sum_date-to': targetDateTo,
        }, 
        sort='sumDate:asc'
    )
    sumDateCategorizedTransactionHeadList = DictionaryUtil.categorizeByKey('sumDate', targetTransactionHeadList)
    
    logger.debug("-----categorized transaction head list-----")
    logger.debug(sumDateCategorizedTransactionHeadList)
    # 分析期間に該当する取引をDBから取得
    # ループでまわし、分析用データを作成する
    # DBにない日付の場合、該当日付の取引をAPIで取得、DBに保存
    # 対象取引データを取得
    # 取得したヘッダを締め日付ごとにみていく
    basketAnalysesRepository = BasketAnalysesRepository
    try:
        basketAnalysis = modelFactory.createBasketAnalysis()
        for sumDate, transactionHeadList in sumDateCategorizedTransactionHeadList.items():
            basket = modelFactory.createBasket()
            for transactionHead in transactionHeadList:
                transactionDetailList = transactionsApi.getTransactionDetail(transactionHead['transactionHeadId'])
                basket.append(transactionDetailList)
            basketAnalysis = modelFactory.createBasketAnalysis()
            basketAnalysis.analysisConditionDate = datetime.datetime.strptime(sumDate, "%Y-%m-%d")
            basketAnalysis.analyzedResult = basket.analyze(rate=10).result

            registeredBasketAnalysis = basketAnalysesRepository.registerBasketAnalysis(basketAnalysis)
            logger.debug("-----register basket analysis-----")
            logger.debug(registeredBasketAnalysis)
       
            basketAnalysisStore = modelFactory.createBasketAnalysisStore()
            basketAnalysisStore.basketAnalysisId = registeredBasketAnalysis.id
            basketAnalysisStore.storeId = targetStoreId
            basketAnalysesRepository.registerBasketAnalysisStore(basketAnalysisStore)
            
        basketAnalysesRepository.commit()

        basketAnalysis = modelFactory.createBasketAnalysis()
        analyzedResultList = basketAnalysis.showByAnalysisConditionDateRange(
            session["contract_id"],
            targetDateFrom,
            targetDateTo
        )
        
        logger.debug("-----analyzed result list-----")
        logger.debug(analyedResultList.string())
        result = analyzedResultList
        ranking = basket.salesRanking(top=3)
        basket.relationRanking("8000002")
        
    #    rules = pyfpgrowth.generate_association_rules(patterns, 0.7)
        storesApi = StoresApi(apiConfig)
        targetStore = storesApi.getStoreById(targetStoreId) 
        logger.info(targetStore)

        pickUpMessage = {
                'from': targetDateFrom,
                'to': targetDateTo,
                'store': targetStore,
        }
        if (len(ranking) != 0):
            pickUpMessage['product1'] = ranking[0]['label']
            pickUpMessage['product2'] = ranking[0]['relations']

    except Exception as e:
        basketAnalysesRepository.rollback()
    
    
    return render_template("baskets/summary.pug",
        contractId = session['contract_id'],
        store = targetStore,
        search_from = targetDateFrom,
        search_to = targetDateTo,
        nodes = result['nodes'],
        edges = result['edges'],
        pickUpMessage = pickUpMessage,
        ranking = ranking
    )
    

