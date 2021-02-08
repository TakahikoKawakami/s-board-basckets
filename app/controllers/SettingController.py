import datetime

from app.config import templates
from app.common.managers import SessionManager, HttpManager
from app.common.abstracts.AbstractController import AbstractController
from app.domains.AccountDomainService import AccountDomainService
from app.domains.BasketDomainService import BasketDomainService
from app.domains.StoreDomainService import StoreDomainService


class AccountStore(AbstractController):
    def __init__(self) ->None:
        super().__init__()

    async def on_get(self, req, resp):
        self._logger.info('get AccountStore')
        storeDomainService = StoreDomainService(self._loginAccount)
        storeList = await storeDomainService.getStoreList()

        jsonEncoded = []
        for store in storeList:
            jsonEncoded.append(await store.serialize)

        resp.media = jsonEncoded
        return
        
    async def on_put(self, req, resp):
        self._logger.info('put AccountStore')
        storeDomainService = StoreDomainService(self._loginAccount)
        await storeDomainService.deleteAllStores()
        await storeDomainService.syncAllStores()

        resp.media = {
            "status": 200
        }
        return

class AccountSetting(AbstractController):
    def __init__(self) ->None:
        super().__init__()

    async def on_get(self, req, resp):
        self._logger.info('get AccountSetting')
        accountSetting = await self._loginAccount.accountSetting
        jsonEncoded = await accountSetting.serialize
        resp.media = jsonEncoded
        return
        
    async def on_post(self, req, resp):
        self._logger.info('post AccountSetting')
        request = await req.media()
        await self._accountDomainService.saveAccountSetting(request)
        resp.media = {
            "status": 200
        }
        return
        # self._basketDomainService = BasketDomainService(self._loginAccount)
        # nowMonth = datetime.datetime.now().month
        # dailyBasketList = await self._basketDomainService.getDailyBasketListByMonth(nowMonth)