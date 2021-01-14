from flask import Blueprint, \
                    render_template,\
                    url_for,\
                    request,\
                    redirect,\
                    jsonify

import logging
import datetime

from common.managers import SessionManager

from baskets.repositories.BasketAnalysesRepository import BasketAnalysesRepository
from baskets.repositories.StoresRepository import StoresRepository
from baskets.entities.Pyfpgrowth import Pyfpgrowth
from baskets.forms.BasketForms import BasketForm


logger = logging.getLogger('flask.app')

route = Blueprint('baskets', __name__, url_prefix='/baskets')

accessToken = None
contractId = None

@route.before_request
def beforeRequest():
    global accessToken
    global contractId

    contractId = SessionManager.getByKey(SessionManager.KEY_CONTRACT_ID)
    accessToken = SessionManager.getByKey(SessionManager.KEY_ACCESS_TOKEN)
    expiresIn = SessionManager.getByKey(SessionManager.KEY_ACCESS_TOKEN_EXPIRES_IN)
    if contractId is None:
        return redirect('/')
    if accessToken is None:
        SessionManager.set(SessionManager.KEY_QUERY_PARAMS_FOR_REDIRECT, request.args)
        _urlWithoutQueryParams = request.url.rstrip("?")
        return redirect(url_for('accounts.getToken') + '?next=' + _urlWithoutQueryParams)
    if expiresIn is not None:
        now = datetime.datetime.now()
        if (expiresIn < now):
            SessionManager.set(SessionManager.KEY_QUERY_PARAMS_FOR_REDIRECT, request.args)
            _urlWithoutQueryParams = request.url.split("?")[0]
            return redirect(url_for('accounts.getToken') + '?next=' + _urlWithoutQueryParams)


@route.route('/index', methods=['GET'])
def index():
    global accessToken
    global contractId

    form = BasketForm(request.args, meta={'csrf': False, 'locales':['ja']})
    storesRepository = StoresRepository().withSmaregiApi(accessToken, contractId)
    storeList = storesRepository.getStoreList()
    form.setStoreList(storeList)
    logger.info(storeList)
    return render_template(
        'baskets/index.pug',
        contractId = contractId,
        form = form,
        message = "",
        stores = storeList
    )


@route.route('/summary', methods=['GET'])
def summary():
    global accessToken
    global contractId

    form = BasketForm(request.args, meta={'csrf': False, 'locales':['ja']})
    storesRepository = StoresRepository().withSmaregiApi(accessToken, contractId)
    storeList = storesRepository.getStoreList()
    
    form.setStoreList(storeList)
    if not form.validate():
        message = "validation error"
        return render_template(
            'baskets/index.pug',
            form = form,
            message = message,
            stores = storeList
        )

    targetStoreId = form.storeField.data
    targetDateFrom = form.dateFromField.data
    targetDateTo = form.dateToField.data

    logger.info("-----search condition-----")
    logger.info("storeId     : " + targetStoreId)
    logger.info("search_from : " + targetDateFrom.strftime("%Y-%m-%d"))
    logger.info("search_to   : " + targetDateTo.strftime("%Y-%m-%d"))

    # 分析期間の日別バスケットリストを取得
    basketAnalysesRepository = BasketAnalysesRepository().withSmaregiApi(accessToken, contractId)
    try:
        dailyBasketListModelList = basketAnalysesRepository.getDailyBasketListByStoreIdAndAnalysisDateRange(
            targetStoreId,
            targetDateFrom,
            targetDateTo
        )
    except Exception as e:
        logger.error(e.args[0])
        return redirect(url_for('baskets.index'))

    # 全データをマージ
    mergedBasketList = []
    for dailyBasketListModel in dailyBasketListModelList:
        mergedBasketList += dailyBasketListModel.basketList
    mergedPyfpgrowthEntity = Pyfpgrowth.createByDataList(mergedBasketList, 0.1)

    vis = None
    if mergedPyfpgrowthEntity is not None:
        logger.debug("-----merged fpgrowth-----")
        # logger.debug(mergedPyfpgrowthEntity.patterns)

        vis = mergedPyfpgrowthEntity.convertToVisJs()
        # vis = mergedPyfpgrowthEntity.result
    
    logger.debug("-----analyzed result list-----")
    logger.debug(vis)
    #basket.relationRanking("8000002")
    
#    rules = pyfpgrowth.generate_association_rules(patterns, 0.7)
    targetStore = storesRepository.getStoreById(targetStoreId) 

    pickUpProductFrom = None
    pickUpProductTo = None
    if (len(mergedPyfpgrowthEntity.result) > 0):
        pickUpProductFrom = mergedPyfpgrowthEntity.result[0]['from']
        pickUpProductTo = mergedPyfpgrowthEntity.result[0]['to']
    pickUpMessage = {
            'store': targetStore,
            'from': targetDateFrom,
            'to': targetDateTo,
            'productFrom': pickUpProductFrom,
            'productTo': pickUpProductTo,
    }

    return render_template("baskets/summary.pug",
        contractId = contractId,
        store = targetStore,
        search_from = targetDateFrom,
        search_to = targetDateTo,
        nodes = vis['nodes'],
        edges = vis['edges'],
        pickUpMessage = pickUpMessage
    )
    
