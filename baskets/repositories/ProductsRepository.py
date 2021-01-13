import common.managers.SessionManager as sessionManager
from common.abstracts.AbstractRepository import AbstractRepository
import datetime
from database import db
from baskets.models.Products import Product as ProductModel

from config import AppConfig
from lib.Smaregi.config import config as SmaregiConfig
from lib.Smaregi.API.POS.ProductsApi import ProductsApi

import logging

class ProductsRepository(AbstractRepository):
    def __init__(self):
        super().__init__()
        
        self._logger = logging.getLogger("flask.app")
        self._appConfig = AppConfig()
        self._apiConfig = SmaregiConfig(
            self._appConfig.ENV_DIVISION,
            self._appConfig.SMAREGI_CLIENT_ID,
            self._appConfig.SMAREGI_CLIENT_SECRET,
            self._logger
        )
        self._apiConfig.accessToken = sessionManager.getByKey(sessionManager.KEY_ACCESS_TOKEN)
        self._apiConfig.contractId = sessionManager.getByKey(sessionManager.KEY_CONTRACT_ID)
        self._productsApi = ProductsApi(self._apiConfig)


    def getProductById(self, _productId):
        _result = db.session.query(ProductModel).filter(
            ProductModel.contract_id == sessionManager.getByKey(sessionManager.KEY_CONTRACT_ID),
            ProductModel.product_id == _productId
        ).first()

        if _result is None:
            _apiResponse = self._productsApi.getProductById(_productId)
            if _apiResponse is not None:
                _productModel = ProductModel()
                _productModel.productId = _apiResponse['productId']
                _productModel.name = _apiResponse['productName']
                _result = self.registerProduct(_productModel)
                self.commit()
        
        return _result


    @staticmethod
    def registerProduct(model):
        model.contractId = sessionManager.getByKey(sessionManager.KEY_CONTRACT_ID)
        model.createdAt = datetime.datetime.now()
        model.modifiedAt = datetime.datetime.now()
        return model.register()