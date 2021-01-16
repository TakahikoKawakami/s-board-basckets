import logging

import common.managers.SessionManager as sessionManager
from common.abstracts.AbstractRepository import AbstractRepository
from lib.Smaregi.API.POS.StoresApi import StoresApi


class StoresRepository(AbstractRepository):
    def __init__(self):
        super().__init__()
        
        self._logger = logging.getLogger("flask.app")


    def getStoreList(self):
        _storesApi = StoresApi(self._apiConfig)
        _apiResponse = _storesApi.getStoreList()
        return _apiResponse


    def getStoreById(self, _storeId):
        _storesApi = StoresApi(self._apiConfig)
        _apiResponse = _storesApi.getStoreById(_storeId)
        return _apiResponse