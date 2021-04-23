from tortoise import fields
from app.common.abstracts.AbstractTortoiseModel import AbstractTortoiseModel

from datetime import datetime
import ujson
import logging

class DailyBasketList(AbstractTortoiseModel):
    """
    バスケット分析用データモデル
    """
    store_id    = fields.IntField(null=False)
    target_date = fields.DateField(null=False)
    basket_list = fields.TextField(null=True, default=[])

    class Meta:
        abstract=False
        table="daily_basket_list"

    def __repr__(self):
        return f'store_id: "{self.store_id}", target_date: "{self.target_date}", basket_list_length: "{len(self.basket_list)}"'

    @property
    def storeId(self) -> int:
        return self.store_id

    @storeId.setter
    def storeId(self, val) -> None:
        self.store_id = val

    @property
    def targetData(self) -> list:
        return self.target_data

    @targetData.setter
    def targetData(self, val:list):
        self.target_data = val

    @property
    def basketList(self) -> list:
        if self.basket_list is None or self.basket_list == []:
            return []
        _result = ujson.loads(self.basket_list)
        return _result
    
    @basketList.setter
    def basketList(self, basketList:list):
        _stringList = DailyBasketList.convertBasketListToString(basketList)
        self.basket_list = ujson.dumps(_stringList)

    def appendBasket(self, basket) -> None:
        _basketList = self.basketList
        _basketList.append(basket.convertListForAnalysis())
        self.basket_list = ujson.dumps(_basketList)

    @staticmethod
    def convertBasketListToString(_basketList:list) -> None:
        """targetData -> targetList に変換します
        """
        _result = []
        for basketModel in _basketList:
            _result.append(basketModel.convertListForAnalysis())
        
        return _result

    @property
    def targetDate(self):
        return self.target_date

    @targetDate.setter
    def targetDate(self, val):
        self.target_date = val

