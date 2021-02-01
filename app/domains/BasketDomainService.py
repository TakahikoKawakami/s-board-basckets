import logging

import app.common.managers.SessionManager as sessionManager
from app.lib.Smaregi.API.POS.TransactionsApi import TransactionsApi

from app.common.abstracts.AbstractDomainService import AbstractDomainService
from app.entities.Baskets import Basket
from app.models.DailyBasketList import DailyBasketList
from app.models.Accounts import AccountSetting

class BasketDomainService(AbstractDomainService):
    def __init__(self, loginAccount):
        super().__init__(loginAccount)
        self.withSmaregiApi(loginAccount.accessToken.accessToken, loginAccount.contractId)

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
                "contract_id": self._loginAccount.contractId,
                "store_id": _basket.storeId,
                "target_date": _basket.targetDate
            }
        )

        _dailyBasketList = _dailyBasketListTuple[0] # [1]は取得したか、作成したかのboolean true: create
        _dailyBasketList.appendBasket(_basket)
        await _dailyBasketList.save()

    async def getDailyBasketListByMonth(self, month: int):
        accountSetting = await AccountSetting.filter(contract_id = self._loginAccount.contractId).first()
        storeId = accountSetting.display_store_id
        _dailyBasketList = await DailyBasketList.filter(
            contract_id = self._loginAccount.contractId,
            target_date__range = (targetDateFrom, targetDateTo)
        )