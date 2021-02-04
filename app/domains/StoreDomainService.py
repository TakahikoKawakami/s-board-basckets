import logging

import app.common.managers.SessionManager as sessionManager
from app.common.abstracts.AbstractDomainService import AbstractDomainService
from app.lib.Smaregi.API.POS.StoresApi import StoresApi
from app.models import Store


class StoreDomainService(AbstractDomainService):
    def __init__(self, loginAccount):
        super().__init__(loginAccount)
        self.withSmaregiApi(loginAccount.accessToken.accessToken, loginAccount.contractId)


    async def getStoreList(self):
        return await Store.filter(
            contract_id = self._loginAccount.contractId
        ).all()

    async def getDisplayStore(self):
        accountSetting = await self._loginAccount.accountSetting
        return await Store.filter(
            contract_id = self._loginAccount.contractId,
            store_id = accountSetting.displayStoreId
        ).first()