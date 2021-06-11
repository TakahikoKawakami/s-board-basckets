import datetime
from logging import Logger

from app.entities.Fpgrowth import Fpgrowth
from app.entities.VisJs import VisJs
from app.models import Store
from app.models import Product
from SmaregiPlatformApi.pos import ProductsApi


class AssociationResult():
    store: Store
    date_from: datetime.datetime
    date_to: datetime.datetime
    fpgrowth: Fpgrowth

    async def vis_js(self) -> VisJs:
        if self.fpgrowth is None:
            raise Exception("fpgrowth is None")
        # self._logger.info("-----convert association result to vis.js-----")
        # self._logger.info(fpgrowth)
        try:
            # self._logger.debug("debug in if content")
            vis = self.fpgrowth.convert_to_vis_js()
            # self._logger.debug("----- ----converted fpgrowth to vis.js-----")
            vis = await self._set_vis_node_label(vis)
            # self._logger.debug("----- ----set label for vis.js-----")
        except Exception as e:
            raise e

        # self._logger.debug("----- ----- vis.js created.")
        return vis

    async def pickup_message(self) -> str:
        productFrom = None
        productTo = None
        if len(self.fpgrowth.result) > 0:
            productFromIdList = [result['id'] for result in self.fpgrowth.result[0]['from']]
            productToIdList = [result['id'] for result in self.fpgrowth.result[0]['to']]
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
        pass

    async def _set_vis_node_label(self, vis: VisJs) -> VisJs:
        productsApi = ProductsApi(self._apiConfig)
        result = VisJs()
        try:
            for node in vis.nodeList:
                product = await Product.filter(
                    contract_id=self._loginAccount.contractId,
                    product_id=node.id
                ).first()
                # self._logger.debug(repr(product))

                if product is None:
                    # self._logger.info("fetching product id: {}".format(node.id))
                    productByApi = productsApi.getProductById(node.id)
                    if productByApi is None:
                        # self._logger.info("productsApi.getProductById is failed.")
                        node.label = "unknown"
                        result.nodeList.append(node)
                        continue
                    # self._logger.debug(productByApi)
                    product = await Product.create(
                        contract_id=self._loginAccount.contractId,
                        product_id=productByApi['productId'],
                        name=productByApi['productName']
                        # color = productByApi['color'],
                        # size = productByApi['size'],
                        # price = productByApi['price']
                    )
                node.label = product.name
                result.nodeList.append(node)
        except Exception as e:
            # self._logger.warning("!!raise exception!!")
            # self._logger.warning(e)
            raise e

        result.edgeList = vis.edgeList
        return result
