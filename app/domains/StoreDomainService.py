import logging

from app.common.abstracts.AbstractDomainService import AbstractDomainService

from SmaregiPlatformApi.pos import StoresApi
from app.models import Store


class StoreDomainService(AbstractDomainService):
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

    async def delete_all_stores(self):
        await Store.filter(
            contract_id=self.login_account.contract_id
        ).delete()

    async def sync_all_stores(self):
        stores_api = StoresApi()
        all_store_list = stores_api.get_store_list()
        print(all_store_list)
        for store in all_store_list:
            await Store.create(
                contract_id=self.login_account.contract_id,
                store_id=store.store_id,
                name=store.store_name
            )
