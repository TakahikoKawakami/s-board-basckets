from sqlalchemy import Column, Integer, Unicode, UnicodeText, ForeignKey, Boolean, Date, DateTime, Enum, Text
from sqlalchemy.orm import relationship, backref
from datetime import datetime
import ujson
import logging
from pprint import pprint, pformat

from entities.Pyfpgrowth import Pyfpgrowth as PyfpgrowthEntity
from database import db
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
        self._targetData = [] # basket entity list
        self._targetList = [] # list for pyfpgrowth
        self._result = {} # result of pyfpgrowth

        self._logger = logging.getLogger('flask.app')


    def __repr__(self):
        return "BasketAnalysis<{}, {}, {}, {}>".format(self.id, self.contractId, self.analysisConditionDate, self.analyzedResult)


    @property
    def targetData(self) -> list:
        return self._targetData


    @targetData.setter
    def targetData(self, val:list):
        self._targetData = val


    @property
    def result(self) -> dict:
        return self._result


    def appendData(self, basketModel) -> None:
        self._targetData.append(basketModel)


    def _convertListToData(self) -> None:
        """targetData -> targetList に変換します
        """
        self._targetList = []
        for basketModel in self._targetData:
            self._targetList.append(basketModel.convertListForAnalysis())


    def analyze(self, rate=1):
        self._convertListToData()
        # 何回出現したデータを対象とするか
        targetCount = len(self._targetList) * rate / 100.0

        # バスケット分析実施 tupple型をキーに持つ辞書を取得する
        patterns = PyfpgrowthEntity.createByDataList(self._targetList, targetCount)
        
        self._logger.info("---- pyfpgrowth find_frequent_patterns ----")
        for line in pformat(patterns).split('\n'):
            self._logger.debug(line)
        
        # pyfpgrowthの結果をそのまま保存
        self.analyzedResult = patterns

        return self

    @property
    def analyzedResult(self):
        return PyfpgrowthEntity.createByPatternJson(self.analyzed_result)


    @analyzedResult.setter
    def analyzedResult(self, _pyfpgrowthEntity):
        """setter

        Arguments:
            _pyfpgrowthEntity {PyfpGrouth} -- baskets.entities.Pyfpgrowthクラス
        """
        self.analyzed_result = _pyfpgrowthEntity.stringPatterns


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


def MockBasketAnalysis():
    pass