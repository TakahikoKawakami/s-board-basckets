from sqlalchemy import Column, Integer, Unicode, UnicodeText, ForeignKey, Boolean, Date, DateTime, Enum, Text
from sqlalchemy.orm import relationship, backref
from datetime import datetime
import ujson
import logging
from pprint import pprint, pformat

from app.entities.Pyfpgrowth import Pyfpgrowth as PyfpgrowthEntity
import app.database as db
from app.common.abstracts.AbstractModel import AbstractModel

class DailyBasketList(AbstractModel):
    """
    バスケット分析用データモデル
    """
    __tablename__ = "daily_basket_list"
    contract_id = Column(Unicode(32), nullable=False)
    basket_list = Column(Text, nullable=False)
    store_id    = Column(Integer, nullable=True)
    target_date = Column(Date, nullable=False)


    #初期化
    def __init__(self):
        self._targetData = [] # basket entity list
        self._targetList = [] # list for pyfpgrowth

        self._logger = logging.getLogger('flask.app')


    def __repr__(self):
        return "DailyBasketList<{}, {}, {}, {}>".format(self.id, self.contractId, self.analysisConditionDate, self.analyzedResult)


    @property
    def storeId(self) -> int:
        return self.store_id

    
    @storeId.setter
    def storeId(self, val) -> None:
        self.store_id = val


    @property
    def targetData(self) -> list:
        return self._targetData


    @targetData.setter
    def targetData(self, val:list):
        self._targetData = val


    @property
    def basketList(self) -> list:
        _result = ujson.loads(self.basket_list)
        return _result

    
    @basketList.setter
    def basketList(self, basketList:list):
        _stringList = DailyBasketList.convertBasketListToString(basketList)
        self.basket_list = ujson.dumps(_stringList)


    def appendData(self, basketModel) -> None:
        """_targetDataにbasketModelを追加します

        Arguments:
            basketModel {Basket} -- [description]
        """
        self._targetData.append(basketModel)


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

