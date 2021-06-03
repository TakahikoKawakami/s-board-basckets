import logging

from app.common.abstracts.AbstractDomainService import AbstractDomainService

from SmaregiPlatformApi.pos import StoresApi
from app.models import Store


class StoreDomainService(AbstractDomainService):
    def __init__(self, login_account):
        super().__init__(login_account)
        self.with_smaregi_api(login_account.access_token_entity.access_token, login_account.contract_id)


    async def get_store_list(self):
        return await Store.filter(
            contract_id=self.login_account.contract_id
        ).all()

    async def get_display_store(self):
        account_setting = await self.login_account.account_setting_model
        return await Store.filter(
            contract_id=self.login_account.contract_id,
            store_id=account_setting.display_store_id
        ).first()

    async def deleteAllStores(self):
        await Store.filter(
            contract_id=self.login_account.contract_id
        ).delete()

    async def syncAllStores(self):
        stores_api = StoresApi(self._api_config)
        all_store_list = storesApi.get_store_list()
        print(all_store_list)
        for store in all_store_list:
            await Store.create(
                contract_id=self.login_account.contractId,
                store_id=store.store_id,
                name=store.store_name
            )
