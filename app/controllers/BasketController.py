import datetime

from marshmallow import ValidationError

from app.config import templates
from app.common.managers import SessionManager, HttpManager
from app.common.abstracts.AbstractController import AbstractController
from app.domains.AccountsDomainService import AccountsDomainService
from app.domains.BasketAssociationDomainService import BasketAssociationDomainService
from app.validators import BasketValidators


class Associate(AbstractController):
    def __init__(self) -> None:
        super().__init__()
        self._basketAssociationDomainService = None

    async def on_get(self, req, resp):
        self._logger.info('access associate')
        if HttpManager.bookRedirect(resp):
            return
        if SessionManager.has(req.session, SessionManager.KEY_ERROR_MESSAGES):
            messages = SessionManager.get(req.session, SessionManager.KEY_ERROR_MESSAGES)
            SessionManager.remove(resp.session, SessionManager.KEY_ERROR_MESSAGES)
            messages = messages
        else:
            messages = ""

        self._basketAssociationDomainService = BasketAssociationDomainService(self._loginAccount)
        storeList = self._basketAssociationDomainService.getStoreList()
        resp.html =  templates.render(
            'baskets/association/index.pug',
            contractId = self._loginAccount.contractId,
            message = messages,
            stores = storeList
        )

class AssociateResult(AbstractController):
    def __init__(self) -> None:
        super().__init__()
        self._basketAssociationDomainService = None

    async def on_get(self, req, resp):
        if HttpManager.bookRedirect(resp):
            self._logger.info('redirect')
            return
        try:
            schema = BasketValidators.AccosiationCondition()
            query = schema.load(req.params)
        except ValidationError as e:
            SessionManager.set(resp.session, SessionManager.KEY_ERROR_MESSAGES, e.messages)
            resp.redirect('/baskets/associate', status_code=302)
            return

        self._basketAssociationDomainService = BasketAssociationDomainService(self._loginAccount)
        targetStore = self._basketAssociationDomainService.getStoreById(query['store_id'])
        fpgrowth = await self._basketAssociationDomainService.associate(
            query['store_id'],
            query['date_from'],
            query['date_to']
        )

        vis = await self._basketAssociationDomainService.convertAssociationResultToVisJs(fpgrowth)
        pickUpMessage = await self._basketAssociationDomainService.convertAssociationResultToPickUpMessage(
            fpgrowth,
            query['store_id'],
            query['date_from'],
            query['date_to']
        )

        visDict = vis.toDict()

        resp.html = templates.render(
            "baskets/association/result.pug",
            contractId = self._loginAccount.contractId,
            store = targetStore,
            search_from = query['date_from'],
            search_to = query['date_to'],
            vis = visDict,
            pickUpMessage = pickUpMessage
        )
        return
