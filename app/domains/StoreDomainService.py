import logging

from app.common.abstracts.AbstractDomainService import AbstractDomainService

from app.repositories import StoresRepository
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
        all_store_list = await StoresRepository.get_all_with_smaregipy()
        await StoresRepository.save_all(all_store_list)
