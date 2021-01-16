import logging

import common.managers.SessionManager as sessionManager
from common.abstracts.AbstractRepository import AbstractRepository


class TransactionsRepository(AbstractRepository):
    def __init__(self):
        super().__init__()
        
        self._logger = logging.getLogger("flask.app")
        self._transactionsApi = TransactionsApi(self._apiConfig)


    def getStoreList(self):
        _apiResponse = self._storesApi.getStoreList()
        return _apiResponse
