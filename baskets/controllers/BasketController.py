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
transactionsApi = TransactionsApi(apiConfig)
storesApi = StoresApi(apiConfig)

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
    targetTransactionHeadList = transactionsApi.getTransaction(
        whereDict={
            'store_id': targetStoreId,
            'sum_date-from': targetDateFrom,
            'sum_date-to': targetDateTo,
        }, 
        sort='sumDate:asc'
    )
    # 締日ごとに並び替え
    sumDateCategorizedTransactionHeadList = DictionaryUtil.categorizeByKey('sumDate', targetTransactionHeadList)
    logger.debug("-----categorized transaction head list-----")
    logger.debug(sumDateCategorizedTransactionHeadList)
    # 分析期間に該当する取引をDBから取得
    # ループでまわし、分析用データを作成する
    # DBにない日付の場合、該当日付の取引をAPIで取得、DBに保存
    # 対象取引データを取得
    # 取得したヘッダを締め日付ごとにみていく
    basketAnalysesRepository = BasketAnalysesRepository(modelFactory)
    try:
        basketAnalysis = modelFactory.createBasketAnalysis()
        for sumDate, transactionHeadList in sumDateCategorizedTransactionHeadList.items():
            # 締め日データが既にあれば無視。なければレコード作成
            existedRecords = BasketAnalysesRepository.getAnalysesByStoreIdAndSumDate(targetStoreId, sumDate)
            if (existedRecords == []):
                _registerBasketAnalysesData(transactionHeadList, targetStoreId, sumDate)
            
        basketAnalysesRepository.commit()
    except Exception as e:
        basketAnalysesRepository.rollback()
        logger.error(e.args[0])
        return redirect(url_for('baskets.index'))
    
    # 指定された期間の分析結果を取得
    basketAnalysis = modelFactory.createBasketAnalysis()
    basketAnalysesList = basketAnalysesRepository.getAnalysesByStoreIdAndAnalysisConditionDateRange(
        targetStoreId,
        targetDateFrom,
        targetDateTo
    )
    if (len(basketAnalysesList) > 0):
        mergedPyfpgrowthEntity = basketAnalysesList[0].analyzedResult
        basketAnalysesList.pop(0)

        for basketAnalysis in basketAnalysesList:
            mergedPyfpgrowthEntity.merge(basketAnalysis.analyzedResult)

    logger.debug("-----merged fpgrowth-----")
    logger.debug(mergedPyfpgrowthEntity.patterns)

    result = mergedPyfpgrowthEntity.convertToVisJs() 
    
    logger.debug("-----analyzed result list-----")
    logger.debug(result["edges"])
    ranking =[]# basket.salesRanking(top=3)
    #basket.relationRanking("8000002")
    
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
    

def _getAndAnalyzeBasketDataByTransactionHeadList(_transactionHeadList, sumDate):
    """取引ヘッダリストに紐づく全取引明細を取得し、バスケット分析モデルを返却します

    Arguments:
        _transactionHeadList {TransactionHead} -- APIで取得した取引ヘッダリスト
        _sumDate {str} -- 締め日（Y-m-d）

    Returns:
        BasketAnalysis -- バスケット分析モデル（分析済）
    """
    
    basketAnalysisModel = modelFactory.createBasketAnalysis()
    for transactionHead in _transactionHeadList:
        transactionDetailList = transactionsApi.getTransactionDetail(transactionHead['transactionHeadId'])
        basketModel = modelFactory.createBasket()
        basketModel.setByTransactionHead(transactionHead)
        basketModel.setByTransactionDetailList(transactionDetailList)
        basketAnalysisModel.appendData(basketModel)
        
    basketAnalysisModel.analysisConditionDate = datetime.datetime.strptime(sumDate, "%Y-%m-%d")
    basketAnalysisModel.analyze(rate=10)
    return basketAnalysisModel


def _registerBasketAnalysesData(_transactionHeadList, _storeId: int, _sumDate: str) -> None:
    """バスケット分析モデルとバスケット分析対象店舗モデルを登録します

    Arguments:
        _transactionHeadList {transactionHead} -- [description]
        _storeId {int} -- [description]
        _sumDate {str} -- [description]
    """
    basketAnalysesRepository = BasketAnalysesRepository(modelFactory)

    basketAnalysis = _getAndAnalyzeBasketDataByTransactionHeadList(_transactionHeadList, _sumDate)
    registeredBasketAnalysis = basketAnalysesRepository.registerBasketAnalysis(basketAnalysis)
    logger.debug("-----register basket analysis-----")
    logger.debug(registeredBasketAnalysis)

    basketAnalysisStore = modelFactory.createBasketAnalysisStore()
    basketAnalysisStore.basketAnalysisId = registeredBasketAnalysis.id
    basketAnalysisStore.storeId = _storeId
    basketAnalysesRepository.registerBasketAnalysisStore(basketAnalysisStore)


def _joinResult(_resultList) -> dict:
    """pyfpgrowth結果のリストを結合します

    Arguments:
        _resultList {[type]} -- [description]
    """
    result = {}
    for eachBasketAnalysis in _resultList:
        pyfpgrowthEntity = eachBasketAnalysis.analyzedResult
        for key, value in pyfpgrowthEntity.patterns.items():
            if not key in result.keys():
                result[key] = 0
            result[key] += value

    return PyfpgrowthEntity


def _convertPyfpgrowthToVisJS(pyfpgrowth):
    pass
        # edges = []
        # nodes = []
        # for k,v in patterns.items():
        #     if (len(k) == 1):
        #         if (k[0].startswith('product__')):
        #             key = k[0].split('product__')[1]
        #             nodes.append({
        #                 "id": key,
        #                 "label": key,
        #                 "value": v
        #             })
        #     elif (len(k) == 2):
        #         if (k[0].startswith('product__') and k[1].startswith('product__')):
        #             key = []
        #             key.append(k[0].split('product__')[1])
        #             key.append(k[1].split('product__')[1])
        #         edges.append({
        #             "from": key[0],
        #             "to": key[1],
        #             "value": v
        #         })
    
        # self._result['nodes'] = nodes
        # self._result['edges'] = edges
