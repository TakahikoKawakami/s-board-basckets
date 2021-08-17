from tortoise import fields
from app.common.abstracts.AbstractTortoiseModel import AbstractTortoiseModel
from app.entities.Baskets import Basket

import ujson


class DailyBasketList(AbstractTortoiseModel):
    """
    バスケット分析用データモデル
    """
    store_id = fields.IntField(null=False)
    target_date = fields.DateField(null=False)
    basket_list = fields.TextField(null=True, default=[])

    class Meta:
        abstract = False
        table = "daily_basket_list"

    def __repr__(self):
        return f'''
            store_id: "{self.store_id}",
            target_date: "{self.target_date}",
            basket_list_length: "{len(self.basket_list)}"
        '''

    @property
    def baskets(self) -> list:
        if self.basket_list is None or self.basket_list == []:
            return []
        _result = ujson.loads(self.basket_list)
        return _result

    @baskets.setter
    def baskets(self, basket_list: list['Basket']):
        string_list = \
            DailyBasketList._convert_basket_list_to_string(basket_list)
        self.basket_list = ujson.dumps(string_list)  # type: ignore

    def append_basket(self, basket: 'Basket') -> None:
        _basket_list = self.baskets
        _basket_list.append(basket.convert_list_for_analysis())
        self.basket_list = ujson.dumps(_basket_list)  # type: ignore

    @staticmethod
    def _convert_basket_list_to_string(basket_list: list) -> list:
        """targetData -> targetList に変換します
        """
        result = []
        for basketModel in basket_list:
            result.append(basketModel.convertListForAnalysis())

        return result
