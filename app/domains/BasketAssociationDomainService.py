from app.common.abstracts.AbstractDomainService import AbstractDomainService

from app.models.DailyBasketList import DailyBasketList
from app.models.Products import Product

from app.entities.Fpgrowth import Fpgrowth
from app.entities.VisJs import VisJs


from SmaregiPlatformApi.pos import StoresApi, ProductsApi

from app.models import Store

class BasketAssociationDomainService(AbstractDomainService):
    def __init__(self, loginAccount):
        super().__init__(loginAccount)
        self.withSmaregiApi(self._loginAccount.accessToken.accessToken, self._loginAccount.contractId)

    @property
    async def targetStore(self) -> 'Store':
        accountSetting = await self._loginAccount.accountSetting
        return await Store.filter(
            contract_id = self._loginAccount.contractId,
            store_id = accountSetting.displayStoreId
        ).first()

    def getStoreList(self):
        _storesApi = StoresApi(self._apiConfig)
        _apiResponse = _storesApi.getStoreList()
        return _apiResponse

    async def associate(self, targetDateFrom, targetDateTo) -> 'Fpgrowth':
        accountSetting = await self._loginAccount.accountSetting
        targetStoreId = str(accountSetting.displayStoreId)
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
        mergedPyfpgrowthEntity = Fpgrowth.createByDataList(mergedBasketList, 0.1, self._logger)
        return mergedPyfpgrowthEntity

    async def convertAssociationResultToVisJs(self, fpgrowth):
        vis = None
        self._logger.info("-----convert association result to vis.js-----")
        self._logger.info(fpgrowth)
        if fpgrowth is not None:
            try:
                self._logger.debug("debug in if content")
                vis = fpgrowth.convertToVisJs()
                self._logger.debug("----- ----converted fpgrowth to vis.js-----")
                vis = await self._setVisNodeLabel(vis)
                self._logger.debug("----- ----set label for vis.js-----")
            except Exception as e:
                raise e
        
        self._logger.debug("----- ----- vis.js created.")
        return vis

    async def _setVisNodeLabel(self, vis):
        productsApi = ProductsApi(self._apiConfig)
        result = VisJs()
        try:
            for node in vis.nodeList:
                product = await Product.filter(
                    contract_id = self._loginAccount.contractId,
                    product_id = node.id
                ).first()
                self._logger.debug(repr(product))

                if product is None:
                    self._logger.info("fetching product id: {}".format(node.id))
                    productByApi = productsApi.getProductById(node.id)
                    if productByApi is None:
                        self._logger.info("productsApi.getProductById is failed.")
                        node.label = "unknown"
                        result.nodeList.append(node)
                        continue
                    self._logger.debug(productByApi)
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
        except Exception as e:
            self._logger.warning("!!raise exception!!")
            self._logger.warning(e)
            raise e

        result.edgeList = vis.edgeList
        return result
    
    async def convertAssociationResultToPickUpMessage(self, fpgrowth, storeId, dateFrom, dateTo):
        store = await self.targetStore

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
