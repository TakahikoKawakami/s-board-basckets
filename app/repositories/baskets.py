import datetime

from app.common.globals import globals
from app.entities.Baskets import Basket
from app.models import DailyBasketList


class DailyBasketListRepository:

    @staticmethod
    async def get_by_store_and_datetime(
        store_id: int,
        datetime: datetime.datetime
    ) -> DailyBasketList:
        _daily_basket_list_tuple = await DailyBasketList.get_or_create(
            contract_id=globals.logged_in_account.contract_id,
            store_id=store_id,
            target_date=datetime
        )

        # [1]は取得したか、作成したかのboolean true: create
        return _daily_basket_list_tuple[0]

    @staticmethod
    async def append_basket_to(
        basket_list: DailyBasketList,
        basket: Basket
    ) -> DailyBasketList:
        basket_list.append_basket(basket)
        await basket_list.save()

        return basket_list
