import datetime

from app.config import templates
from app.common.managers import SessionManager, HttpManager
from app.common.abstracts.AbstractController import AbstractController
from app.domains.AccountDomainService import AccountDomainService
from app.domains.BasketDomainService import BasketDomainService


class AccountSetting(AbstractController):
    def __init__(self) ->None:
        super().__init__()

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