import datetime

from marshmallow import ValidationError

from app.common.managers import SessionManager, HttpManager
from app.common.abstracts.AbstractController import AbstractController
from app.domains.AccountDomainService import AccountDomainService
from app.domains.BasketAssociationDomainService import BasketAssociationDomainService
from app.domains.BasketDomainService import BasketDomainService
from app.validators import BasketValidators


class Basket(AbstractController):
    def __init__(self) ->None:
        super().__init__()
        self._basketDomainService = None

    async def on_get(self, req, resp):
        if self.isBookingRedirect():
            return
        self._logger.info('access DailyBasket')
        self._basketDomainService = BasketDomainService(self._loginAccount)
        if req.params != {}:
            startDate = datetime.datetime.strptime(req.params['startDate'], "%Y-%m-%dT%H:%M:%S%z").date()
            endDate = datetime.datetime.strptime(req.params['endDate'], "%Y-%m-%dT%H:%M:%S%z").date()
            dailyBasketList = await self._basketDomainService.getDailyBasketListByDateRange(startDate, endDate)

            jsonDailyBasketList = [await model.serialize for model in dailyBasketList]
            resp.media = jsonDailyBasketList
            return
        else:
            await self.render('baskets/index.pug')

    async def on_put(self, req, resp):
        if self.isAccessDenied():
            return
        self._logger.info('sync DailyBasket')
        self._basketDomainService = BasketDomainService(self._loginAccount)
        request = await req.media(format='json')
        dateFrom = request['startDate'] + 'T00:00:00+0900'
        dateTo = request['endDate'] + 'T23:59:59+0900'
        try:
            syncedDailyBasketList = await self._basketDomainService.syncDailyBasketListByDateRange(dateFrom ,dateTo)
            # jsonDailyBasketList = [await model.serialize for model in syncedDailyBasketList]
            # resp.media = jsonDailyBasketList
        except Exception:
            resp.status_code = 400

    async def on_delete(self, req, resp):
        self._logger.info('delete DailyBasket')
        self._basketDomainService = BasketDomainService(self._loginAccount)
        request = req.params
        dateFrom = request['startDate']
        dateTo = request['endDate']
        try:
            await self._basketDomainService.deleteDailyBasketListByDateRange(dateFrom ,dateTo)
        except Exception:
            resp.status_code = 400
        
        
class Associate(AbstractController):
    def __init__(self) -> None:
        super().__init__()
        self._basketAssociationDomainService = None

    async def on_get(self, req, resp):
        if self.isBookingRedirect():
            return
        self._logger.info('access associate')
        self._logger.info(await self._loginAccount.accountSetting)
        if self.isBookingRedirect():
            return

        await self.render(
            'baskets/association/index.pug'
        )

class AssociateResult(AbstractController):
    """分析結果コントローラ

    Args:
        AbstractController ([type]): [description]
    """
    def __init__(self) -> None:
        super().__init__()
        self._basketAssociationDomainService = None

    async def on_get(self, req, resp):
        if self.isBookingRedirect():
            return
        try:
            schema = BasketValidators.AccosiationCondition()
            query = schema.load(req.params)

            self._basketAssociationDomainService = await BasketAssociationDomainService.createInstance(self._loginAccount)
            targetStore = await self._basketAssociationDomainService.targetStore
            fpgrowth = await self._basketAssociationDomainService.associate(query['date_from'], query['date_to'])
            self._logger.info('create fpgrowth')

            vis = await self._basketAssociationDomainService.convertAssociationResultToVisJs(fpgrowth)
            self._logger.info('create vis')

            pickUpMessage = await self._basketAssociationDomainService.convertAssociationResultToPickUpMessage(
                fpgrowth,
                targetStore.storeId,
                query['date_from'],
                query['date_to']
            )
            self._logger.info('create pickup messages')

            visDict = vis.toDict()

            await self.render(
                path = "baskets/association/result.pug",
                search_from = query['date_from'],
                search_to = query['date_to'],
                vis = visDict,
                pickUpMessage = pickUpMessage,
            )
            return

        except ValidationError as e:
            SessionManager.set(resp.session, SessionManager.KEY_ERROR_MESSAGES, e.messages)
            resp.redirect('/baskets', status_code=302)
            return
        except Exception as e:
            SessionManager.set(resp.session, SessionManager.KEY_ERROR_MESSAGES, e.messages)
            resp.redirect('/baskets', status_code=302)
            return