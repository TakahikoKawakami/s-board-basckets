import logging

import app.common.managers.SessionManager as sessionManager
from app.common.abstracts.AbstractRepository import AbstractRepository
from app.lib.Smaregi.API.POS.TransactionsApi import TransactionsApi


class TransactionsRepository(AbstractRepository):
    def __init__(self):
        super().__init__()
        
        self._logger = logging.getLogger("flask.app")


    def getTransactionById(self, _id):
        _transactionsApi = TransactionsApi(self._apiConfig)
        whereDict = {
            'with_details': 'all'
        }
        _apiResponse = _transactionsApi.getTransaction(_id, whereDict=whereDict)
        return _apiResponse

