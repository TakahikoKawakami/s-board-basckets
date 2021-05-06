from flask import session
from sqlalchemy import Column, Integer, Unicode, UnicodeText, ForeignKey, Boolean, DateTime, Enum, Text
from sqlalchemy.orm import relationship, backref
from pprint import pprint
import json
from datetime import datetime

import database as db
from common.abstracts.AbstractModel import AbstractModel


import logging


class BasketAnalysisStore(AbstractModel):
    """
    バスケット分析対象店舗モデル
    """
    __tablename__ = "basket_analysis_store"
    
    daily_basket_list_id = Column(Unicode(32), ForeignKey('daily_basket_list.id'), nullable=False)
    store_id = Column(Unicode(32), nullable=False)


    #初期化
    def __init__(self):
        pass


    def __repr__(self):
        return "BasketAnalysisStore<{}, {}, {}, {}>".format(self.id, self.contractId, self.basketAnalysisId, self.storeId)


    @property
    def storeId(self):
        return self.store_id


    @storeId.setter
    def storeId(self, val):
        self.store_id = val
    

    @property
    def basketAnalysisId(self):
        return self.basket_analysis_id


    @basketAnalysisId.setter
    def basketAnalysisId(self, val):
        self.basket_analysis_id = val


    def showByProductId(self, _contractId, _productId):
        product = db.session.query(self).filter(
            self.contract_id == _contractId,
            self.id == _productId
        ).first()
        return account