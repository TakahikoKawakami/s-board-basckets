import logging

import app.common.managers.SessionManager as sessionManager
from app.lib.Smaregi.API.POS.TransactionsApi import TransactionsApi

from app.common.abstracts.AbstractDomainService import AbstractDomainService
from app.entities.Baskets import Basket
from app.models.DailyBasketList import DailyBasketList

class BasketDomainService(AbstractDomainService):
    def __init__(self, loginAccount):
        self._logger = logging.getLogger(__name__)
        self.withSmaregiApi(loginAccount.accessToken.accessToken, loginAccount.contractId)

        self.loginAccount = loginAccount

    async def registerBasketByTransactionHeadId(self, transactionHeadId):
        _transactionsApi = TransactionsApi(self._apiConfig)
        whereDict = {
            'with_details': 'all'
        }
        _apiResponse = _transactionsApi.getTransaction(transactionHeadId, whereDict=whereDict)
        _basket = Basket()
        _basket.setByTransactionHead(_apiResponse)
        _basket.setByTransactionDetailList(_apiResponse['details'])

        _dailyBasketListTuple = await DailyBasketList.get_or_create(
            {
                "contract_id": self.loginAccount.contractId,
                "store_id": _basket.storeId,
                "target_date": _basket.targetDate
            }
        )

        _dailyBasketList = _dailyBasketListTuple[0] # [1]は取得したか、作成したかのboolean true: create
        _dailyBasketList.appendBasket(_basket)
        await _dailyBasketList.save()

