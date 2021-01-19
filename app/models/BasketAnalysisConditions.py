from sqlalchemy import Column, Integer, Unicode, UnicodeText, ForeignKey, Boolean, DateTime, Enum, Text
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from pprint import pprint
import json

import database as db
from common.abstracts import AbstractModel

import pyfpgrowth
import logging

class BasketAnalysisCondition(AbstractModel):
    """
    バスケット分析条件モデル
    """
    __tablename__ = "basket_analysis_condition"
    contract_id = Column(Unicode(32), nullable=False)
    basket_analysis_id = Column(Unicode(32), ForeignKey('basket_analysis.id'), nullable=False)
    conditions = Column(Text, nullable=False)


    #初期化
    def __init__(self):
        pass


    def __repr__(self):
        return "BasketAnalysis<{}, {}, {}>".format(self.id, self.contractId, self.analyzedResult)


    @property
    def contractId(self):
        return self.contract_id


    @property
    def conditions(self):
        return self.conditions
    

    @conditions.setter
    def conditions(self, val):
        self.conditions = json.dumps(val)


    @property
    def analysisConditionId(self):
        reutrn = self.analysis_condition_id


    def register(self):
        # insert into users(name, address, tel, mail) values(...)
        self.created_at = datetime.datetime.now()
        self.modified_at = datetime.datetime.now()
        db.session.add(self)
        return self
    

    def delete(self):
        db.session.delete(self)
        return self


    def showByProductId(self, _contractId, _productId):
        product = db.session.query(self).filter(
            self.contract_id == _contractId,
            self.id == _productId
        ).first()
        return account