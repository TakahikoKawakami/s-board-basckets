import datetime

from marshmallow import ValidationError

from app.common.managers import SessionManager
from app.common.abstracts.AbstractController import AbstractController
from app.domains.BasketAssociationDomainService import BasketAssociationDomainService
from app.domains.BasketDomainService import BasketDomainService
from app.validators import BasketValidators


class Basket(AbstractController):
    def __init__(self) -> None:
        super().__init__()
        self._basket_domain_service = None

    async def on_get(self, req, resp):
        if self.is_booking_redirect():
            return
        self._logger.info('access DailyBasket')
        self._basket_domain_service = BasketDomainService(self.login_account)
        if req.params != {}:
            start_date = datetime.datetime.strptime(
                req.params['startDate'],
                "%Y-%m-%dT%H:%M:%S%z"
            ).date()
            end_date = datetime.datetime.strptime(
                req.params['endDate'],
                "%Y-%m-%dT%H:%M:%S%z"
            ).date()
            daily_basket_list = \
                await self.\
                _basket_domain_service.\
                get_daily_basket_list_by_date_range(start_date, end_date)

            json_daily_basket_list = [
                await model.serialize()
                for model in daily_basket_list
            ]
            resp.media = json_daily_basket_list
            return
        else:
            await self.render('baskets/index.pug')


class AssociateResult(AbstractController):
    """分析結果コントローラ

    Args:
        AbstractController ([type]): [description]
    """
    def __init__(self) -> None:
        super().__init__()
        self._basket_association_domainService = None

    async def on_get(self, req, resp):
        if self.is_booking_redirect():
            return
        try:
            schema = BasketValidators.AccosiationCondition()
            query = schema.load(req.params)

            account_setting = await self.login_account.account_setting_model
            target_store_id = str(account_setting.display_store_id)

            # basket_domain_service = \
            #     await BasketDomainService\
            #     .create_instance(self.login_account)
            # association_result = await basket_domain_service.associate(
            #     target_store_id,
            #     query['date_fronm'],
            #     query['date_to']
            # )

            # vis = await association_result.vis_js()
            # pickup_message = association_result.pickup_message()

            # await self.render(
            #     path="baskets/association/result.pug",
            #     search_from=query['date_from'],
            #     search_to=query['date_to'],
            #     vis=vis.toDict(),
            #     pickUpMessage=pickup_message
            # )
            # return

            self._basket_association_domain_service = \
                await BasketAssociationDomainService\
                .create_instance(self.login_account)
            targetStore = await self\
                ._basket_association_domain_service\
                .target_store

            fpgrowth = await self._basket_association_domain_service\
                .associate(query['date_from'], query['date_to'])
            self._logger.info('create fpgrowth')

            vis = await self\
                ._basket_association_domain_service\
                .convert_association_result_to_vis_js(fpgrowth)
            self._logger.info('create vis')

            pickUpMessage = await self\
                ._basket_association_domain_service\
                .convert_association_result_to_pickup_message(
                    fpgrowth,
                    targetStore.storeId,
                    query['date_from'],
                    query['date_to']
                )
            self._logger.info('create pickup messages')

            visDict = vis.toDict()

            await self.render(
                path="baskets/association/result.pug",
                search_from=query['date_from'],
                search_to=query['date_to'],
                vis=visDict,
                pickUpMessage=pickUpMessage,
            )
            return

        except ValidationError as e:
            SessionManager.set(
                resp.session,
                SessionManager.KEY_ERROR_MESSAGES,
                e.messages
            )
            resp.redirect('/baskets', status_code=302)
            return
        except Exception as e:
            SessionManager.set(
                resp.session,
                SessionManager.KEY_ERROR_MESSAGES,
                e.messages
            )
            resp.redirect('/baskets', status_code=302)
            return
