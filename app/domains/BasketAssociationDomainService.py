from typing import Optional
from enum import Enum, IntEnum, auto
from app.common.abstracts.AbstractDomainService import AbstractDomainService

from app.models.DailyBasketList import DailyBasketList
from app.models.Products import Product

from app.entities.Fpgrowth import Fpgrowth
from app.entities.VisJs import VisJs
from app.entities.Baskets import Basket


from app.repositories import ProductsRepository

from app.models import Store


class BasketAssociationDomainService(AbstractDomainService):
    class AnalyzeTypeEnum(IntEnum):
        PRODUCT_PRODUCT = 0
        CUSTOMERGROUP_PRODUCT = auto()

    @property
    async def target_store(self) -> Optional['Store']:
        account_setting = await self.login_account.account_setting_model
        return await Store.filter(
            contract_id=self.login_account.contract_id,
            store_id=account_setting.display_store_id
        ).first()

    async def associate(
        self,
        analyze_type: int,
        target_store_id: str,
        targetDateFrom,
        targetDateTo
    ) -> 'Fpgrowth':
        self._logger.info("-----search condition-----")
        self._logger.info("analyze_type : " + str(analyze_type))
        self._logger.info("storeId      : " + target_store_id)
        self._logger.info("search_from  : " + targetDateFrom.strftime("%Y-%m-%d"))
        self._logger.info("search_to    : " + targetDateTo.strftime("%Y-%m-%d"))

        # 分析期間の日別バスケットリストを取得
        dailyBasketListModelList = await DailyBasketList.filter(
            contract_id=self.login_account.contract_id,
            store_id=target_store_id,
            target_date__range=(targetDateFrom, targetDateTo)
        )

        # 全データをマージ
        mergedBasketList = []
        for dailyBasketListModel in dailyBasketListModelList:
            mergedBasketList += dailyBasketListModel.baskets
        target_field_list = []
        if analyze_type == BasketAssociationDomainService.AnalyzeTypeEnum.PRODUCT_PRODUCT:
            target_field_list = [
                Basket.PREFIXES_PRODUCT,
                Basket.PREFIXES_PRODUCT,
            ]
        elif analyze_type == BasketAssociationDomainService.AnalyzeTypeEnum.CUSTOMERGROUP_PRODUCT:
            target_field_list = [
                Basket.PREFIXES_CUSTOMER_GROUP,
                Basket.PREFIXES_PRODUCT,
            ]

        mergedPyfpgrowthEntity = Fpgrowth.createByDataList(
            mergedBasketList,
            target_field_list,
            0.1,
            self._logger
        )
        return mergedPyfpgrowthEntity

    async def convert_association_result_to_vis_js(self, fpgrowth: Fpgrowth):
        vis = None
        self._logger.info("-----convert association result to vis.js-----")
        self._logger.info(fpgrowth)
        if fpgrowth is not None:
            try:
                self._logger.debug("debug in if content")
                vis = fpgrowth.convert_to_vis_js()
                self._logger.debug("----- ----converted fpgrowth to vis.js-----")
                vis = await self._set_vis_node_label(vis)
                self._logger.debug("----- ----set label for vis.js-----")
            except Exception as e:
                raise e
        
        self._logger.debug("----- ----- vis.js created.")
        return vis

    async def _set_vis_node_label(self, vis):
        result = VisJs()
        try:
            for node in vis.nodeList:
                # product = await Product.filter(
                #     contract_id=self.login_account.contract_id,
                #     product_id=node.id
                # ).first()
                # self._logger.debug(repr(product))

                if node.type_prefix == Basket.PREFIXES_PRODUCT:
                    self._logger.info(
                        "fetching product id: {}".format(node.id)
                    )
                    # productByApi = productsApi.get_product_by_id(node.id)
                    productByApi = await ProductsRepository.get_by_id(node.id)
                    if productByApi is None:
                        self._logger.info(
                            "productsApi.getProductById is failed."
                        )
                        node.label = "unknown"
                        result.nodeList.append(node)
                        continue
                    self._logger.debug(productByApi)
                    # product = await Product.create(
                    #     contract_id=self.login_account.contract_id,
                    #     product_id=productByApi.product_id,
                    #     name=productByApi.product_name
                    #     # color = productByApi['color'],
                    #     # size = productByApi['size'],
                    #     # price = productByApi['price']
                    # )
                    node.label = productByApi.product_name
                elif node.type_prefix == Basket.PREFIXES_CUSTOMER_GROUP:
                    self._logger.info(
                        "fetching customer group id: {}".format(node.id)
                    )
                    productByApi = await ProductsRepository.get_by_id(node.id)
                    if productByApi is None:
                        self._logger.info(
                            "CustomerGroupApi.getCustomerGroupById is failed."
                        )
                        node.label = "unknown"
                        result.nodeList.append(node)
                        continue
                    self._logger.debug(productByApi)
                    # product = await Product.create(
                    #     contract_id=self.login_account.contract_id,
                    #     product_id=productByApi.product_id,
                    #     name=productByApi.product_name
                    #     # color = productByApi['color'],
                    #     # size = productByApi['size'],
                    #     # price = productByApi['price']
                    # )
                    node.label = productByApi.product_name
                result.nodeList.append(node)
        except Exception as e:
            self._logger.warning("!!raise exception!!")
            self._logger.warning(e)
            raise e

        result.edgeList = vis.edgeList
        return result

    async def convert_association_result_to_pickup_message(
        self,
        fpgrowth,
        storeId,
        date_from,
        date_to
    ):
        store = await self.target_store

        product_from = None
        product_to = None
        if len(fpgrowth.result) > 0:
            product_from_id_list = [
                result['id']
                for result in fpgrowth.result[0]['from']
            ]
            product_to_id_list = [
                result['id']
                for result in fpgrowth.result[0]['to']
            ]
            product_from = await Product.filter(
                contract_id=self.login_account.contract_id,
                product_id__in=product_from_id_list
            ).all()
            product_to = await Product.filter(
                contract_id=self.login_account.contract_id,
                product_id__in=product_to_id_list
            ).all()
        message = {
            'store': store,
            'from': date_from,
            'to': date_to,
            'productFrom': product_from,
            'productTo': product_to,
        }
        return message
