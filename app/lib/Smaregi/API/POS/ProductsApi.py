from urllib.parse import urlencode

from .entities import Product
from ..BaseServiceApi import BaseServiceApi


class ProductsApi(BaseServiceApi):
    def __init__(self, config):
        super().__init__(config)


    def __repr__(self):
        # return '<{}, {}, {}>".format(self.id, self.)"'
        pass


    def getProductById(self, id: int, field = None, sort = None, whereDict:dict = None) -> 'Product':
        """商品取得APIを実施します

        Raises:
            Exception: 取得できなかった場合

        Returns:
            Product: [description]
        """
        contractId = self.config.contractId
        self.uriPos = self.config.uriApi + '/' + contractId + '/pos'
        self.uri = self.uriPos + '/products/' + id
        
        header = self._getHeader()
        body = self._getQueryForDetail('productId,productName', sort, whereDict)
        
        response = self._apiGet(self.uri, header, body)
        if response[0] != 200:
            raise Exception(response[1])
        return Product(response[1])
