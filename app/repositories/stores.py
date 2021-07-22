from typing import TypeVar, Type, List

from smaregipy.pos import StoreCollection

from app.common.globals import globals
from app.entities import Store as StoreEntity
from app.models import Store


T = TypeVar('T', bound='StoresRepository')


class StoresRepository:
    @classmethod
    async def get_all_with_smaregipy(cls: Type[T]) -> List[StoreEntity]:
        store_collection = await StoreCollection().get_all()

        result = []
        for store in store_collection.records.values():
            result.append(StoreEntity(store.store_id, store.store_name))
        return result

    @classmethod
    async def save_all(cls: Type[T], store_list: List[StoreEntity]) -> bool:
        for store in store_list:
            await Store.create(
                contract_id=globals.logged_in_account.contract_id,
                store_id=store.store_id,
                name=store.store_name
            )
