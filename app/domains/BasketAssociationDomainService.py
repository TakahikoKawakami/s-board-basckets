from app.common.abstracts.AbstractDomainService import AbstractDomainService
from app.common.managers import SessionManager
from app.common.utils import DictionaryUtil

from app.models.DailyBasketList import DailyBasketList
from app.models.Products import Product

from app.entities.Fpgrowth import Fpgrowth
from app.entities.VisJs import VisJs

import datetime

from app.lib.Smaregi.API.POS.StoresApi import StoresApi
from app.lib.Smaregi.API.POS.ProductsApi import ProductsApi

class BasketAssociationDomainService(AbstractDomainService):
    def __init__(self, loginAccount):
        super().__init__(loginAccount)
        self.withSmaregiApi(self._loginAccount.accessToken.accessToken, self._loginAccount.contractId)

    @property
    def targetStore(self):
        _storesApi = StoresApi(self._apiConfig)
        _apiResponse = _storesApi.getStoreById(self._loginAccount.account_setting.displayStoreId)
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
            contract_id = self._loginAccount.contractId,
            store_id = targetStoreId,
            target_date__range = (targetDateFrom, targetDateTo)
        )

        # 全データをマージ
        mergedBasketList = []
        for dailyBasketListModel in dailyBasketListModelList:
            mergedBasketList += dailyBasketListModel.basketList
        mergedPyfpgrowthEntity = Fpgrowth.createByDataList(mergedBasketList, 0.1)
        return mergedPyfpgrowthEntity

    async def convertAssociationResultToVisJs(self, fpgrowth):
        vis = None
        if fpgrowth is not None:
            # logger.debug("-----merged fpgrowth-----")
            # logger.debug(mergedPyfpgrowthEntity.patterns)
            vis = fpgrowth.convertToVisJs()
            vis = await self._setVisNodeLabel(vis)
        
        return vis

    async def _setVisNodeLabel(self, vis):
        productsApi = ProductsApi(self._apiConfig)
        result = VisJs()
        for node in vis.nodeList:
            product = await Product.filter(
                contract_id = self._loginAccount.contractId,
                product_id = node.id
            ).first()
            if product is None:
                productByApi = productsApi.getProductById(node.id)
                product = await Product.create(
                    contract_id = self._loginAccount.contractId,
                    product_id = productByApi['productId'],
                    name = productByApi['productName']
                    # color = productByApi['color'],
                    # size = productByApi['size'],
                    # price = productByApi['price']
                )
            node.label = product.name
            result.nodeList.append(node)
        result.edgeList = vis.edgeList
        return result
    
    async def convertAssociationResultToPickUpMessage(self, fpgrowth, storeId, dateFrom, dateTo):
        storesApi = StoresApi(self._apiConfig)
        store = storesApi.getStoreById(storeId)

        productFrom = None
        productTo = None
        if len(fpgrowth.result) > 0:
            productFromIdList = [result['id'] for result in fpgrowth.result[0]['from']]
            productToIdList = [result['id'] for result in fpgrowth.result[0]['to']]
            productFrom = await Product.filter(
                contract_id = self._loginAccount.contractId,
                product_id__in = productFromIdList
            ).all()
            productTo = await Product.filter(
                contract_id = self._loginAccount.contractId,
                product_id__in = productToIdList
            ).all()
        message = {
            'store': store,
            'from': dateFrom,
            'to': dateTo,
            'productFrom': productFrom,
            'productTo': productTo,
        }
        return message