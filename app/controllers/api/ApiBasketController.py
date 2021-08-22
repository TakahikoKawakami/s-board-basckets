import datetime

from marshmallow import ValidationError

from app.common.managers import SessionManager
from app.common.abstracts.AbstractController import AbstractController
from app.domains.BasketAssociationDomainService import BasketAssociationDomainService
from app.domains.BasketDomainService import BasketDomainService
from app.validators import BasketValidators


class ApiBasket(AbstractController):
    def __init__(self) -> None:
        super().__init__()
        self._basket_domain_service = None

    async def on_get(self, req, resp):
        if self.is_booking_redirect():
            return
        self._logger.info('get basket')
        self._basket_domain_service = \
            await BasketDomainService.create_instance(self.login_account)
        if req.params != {}:
            start_date = datetime.datetime.strptime(
                req.params['startDate'],
                "%Y-%m-%dT%H:%M:%S%z"
            ).date()
            end_date = datetime.datetime.strptime(
                req.params['endDate'],
                "%Y-%m-%dT%H:%M:%S%z"
            ).date()
            daily_basket_list = await self\
                ._basket_domain_service\
                .get_daily_basket_list_by_date_range(start_date, end_date)

            json_daily_basket_list = [
                await model.serialize()
                for model in daily_basket_list
            ]
            resp.media = json_daily_basket_list
            return
        else:
            resp.media = {}
            return

    async def on_put(self, req, resp):
        """取引明細一覧CSV作成APIを利用して、スマレジの取引データを同期します

        Args:
            req ([type]): [description]
            resp ([type]): [description]
        """
        if self.is_access_denied():
            return
        self._logger.info('sync DailyBasket')
        self._basket_domain_service = await BasketDomainService.create_instance(self.login_account)
        request = await req.media(format='json')
        date_from = request['startDate'] + 'T00:00:00+0900'
        date_to = request['endDate'] + 'T23:59:59+0900'
        try:
            await self._basket_domain_service.sync_daily_basket_list_by_date_range(date_from, date_to)
        except Exception:
            resp.status_code = 400

    async def on_delete(self, req, resp):
        self._logger.info('delete DailyBasket')
        self._basket_domain_service = await BasketDomainService.create_instance(self.login_account)
        request = req.params
        date_from = request['startDate']
        date_to = request['endDate']
        try:
            await self._basket_domain_service.delete_daily_basket_list_by_date_range(date_from, date_to)
        except Exception:
            resp.status_code = 400
        
        
class ApiAssociate(AbstractController):
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

class ApiAssociateResult(AbstractController):
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
