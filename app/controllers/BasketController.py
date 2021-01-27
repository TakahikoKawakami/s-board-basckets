from marshmallow import ValidationError

import logging
import datetime

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
        if HttpManager.bookRedirect(resp):
            return
        if SessionManager.has(req.session, SessionManager.KEY_ERROR_MESSAGES):
            messages = SessionManager.get(req.session, SessionManager.KEY_ERROR_MESSAGES)
        else:
            messages = ""

        self._basketAssociationDomainService = BasketAssociationDomainService(self._loginAccount)
        storeList = self._basketAssociationDomainService.getStoreList()
        resp.html =  templates.render(
            'baskets/index.pug',
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
        vis = await self._basketAssociationDomainService.associate(
            query['store_id'],
            query['date_from'],
            query['date_to']
        )

        visDict = vis.toDict()

        resp.html = templates.render(
            "baskets/summary.pug",
            contractId = self._loginAccount.contractId,
            store = targetStore,
            search_from = query['date_from'],
            search_to = query['date_to'],
            vis = visDict,
            pickUpMessage = ""
        )
        return
