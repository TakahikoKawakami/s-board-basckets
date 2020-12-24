from sqlalchemy import Column, Integer, Unicode, UnicodeText, ForeignKey, Boolean, Date, DateTime, Enum, Text
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from pprint import pprint
from datetime import datetime
import json
from database import db

import pyfpgrowth
import logging
from common.abstracts.AbstractModel import AbstractModel

class BasketAnalysis(AbstractModel):
    """
    バスケット分析結果モデル
    """
    __tablename__ = "basket_analysis"
    contract_id = Column(Unicode(32), nullable=False)
    analyzed_result = Column(Text, nullable=False)
    analysis_condition_date = Column(Date, nullable=False)


    #初期化
    def __init__(self):
        pass


    def __repr__(self):
        return "BasketAnalysis<{}, {}, {}, {}>".format(self.id, self.contractId, self.analysisConditionDate, self.analyzedResult)


    @property
    def analyzedResult(self):
        return json.loads(self.analyzed_result)


    @analyzedResult.setter
    def analyzedResult(self, val):
        self.analyzed_result = json.dumps(val)


    @property
    def analysisConditionDate(self):
        return self.analysis_condition_date


    @analysisConditionDate.setter
    def analysisConditionDate(self, val):
        self.analysis_condition_date = val


    def showByAnalysisConditionDateRange(self, _contractId, _analysisConditionDateFrom, _analysisConditionDateTo):
        result = db.session.query(BasketAnalysis).filter(
            BasketAnalysis.contract_id == _contractId,
            db.func.date(BasketAnalysis.analysis_condition_date) >= _analysisConditionDateFrom,
            db.func.date(BasketAnalysis.analysis_condition_date) <= _analysisConditionDateTo,
        ).all()
        return result 