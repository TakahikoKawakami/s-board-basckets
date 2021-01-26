from app.common.abstracts.AbstractDomainService import AbstractDomainService
from app.common.managers import SessionManager
from app.common.utils import DictionaryUtil

from app.models.DailyBasketList import DailyBasketList

from app.entities.Fpgrowth import Fpgrowth
from app.entities.VisJs import VisJs

import datetime
import logging

from app.lib.Smaregi.API.POS.StoresApi import StoresApi
from app.lib.Smaregi.API.POS.ProductsApi import ProductsApi

class BasketAssociationDomainService(AbstractDomainService):
    def __init__(self, loginAccount):
        self._logger = logging.getLogger(__name__)
        self.withSmaregiApi(loginAccount.accessToken.accessToken, loginAccount.contractId)

        self.loginAccount = loginAccount

    def getStoreById(self, storeId):
        _storesApi = StoresApi(self._apiConfig)
        _apiResponse = _storesApi.getStoreById(storeId)
        return _apiResponse

    def getStoreList(self):
        _storesApi = StoresApi(self._apiConfig)
        _apiResponse = _storesApi.getStoreList()
        return _apiResponse

    async def associate(self, targetStoreId: int, targetDateFrom, targetDateTo):
        self._logger.info("-----search condition-----")
        self._logger.info("storeId     : " + targetStoreId)
        self._logger.info("search_from : " + targetDateFrom.strftime("%Y-%m-%d"))
        self._logger.info("search_to   : " + targetDateTo.strftime("%Y-%m-%d"))

        # 分析期間の日別バスケットリストを取得
        dailyBasketListModelList = await DailyBasketList.filter(
            contract_id = self.loginAccount.contractId,
            store_id = targetStoreId,
            target_date__range = (targetDateFrom, targetDateTo)
        )

        # 全データをマージ
        mergedBasketList = []
        for dailyBasketListModel in dailyBasketListModelList:
            mergedBasketList += dailyBasketListModel.basketList
        mergedPyfpgrowthEntity = Fpgrowth.createByDataList(mergedBasketList, 0.1)

        vis = None
        if mergedPyfpgrowthEntity is not None:
            # logger.debug("-----merged fpgrowth-----")
            # logger.debug(mergedPyfpgrowthEntity.patterns)

            vis = mergedPyfpgrowthEntity.convertToVisJs()
            vis = self._setVisNodeLabel(vis)
            # vis = mergedPyfpgrowthEntity.result
        
        # logger.debug("-----analyzed result list-----")
        # logger.debug(vis)
        #basket.relationRanking("8000002")
        
    #    rules = pyfpgrowth.generate_association_rules(patterns, 0.7)
        return vis

    def _setVisNodeLabel(self, vis):
        productsApi = ProductsApi(self._apiConfig)
        result = VisJs()
        for node in vis.nodeList:
            productName = productsApi.getProductById(node.id)['productName']
            node.label = productName
            result.nodeList.append(node)
        result.edgeList = vis.edgeList
        return result