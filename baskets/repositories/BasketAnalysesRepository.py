import common.managers.SessionManager as sessionManager
from common.abstracts.AbstractRepository import AbstractRepository
from datetime import datetime
from baskets.models.DailyBasketList import DailyBasketList
from baskets.models.BasketAnalyses import BasketAnalysis
from baskets.models.BasketAnalysisConditions import BasketAnalysisCondition
from database import db

class BasketAnalysesRepository(AbstractRepository):
    def __init__(self, modelFactory):
        super().__init__()


    @staticmethod
    def registerBasketAnalysis(model):
        model.contractId = sessionManager.getByKey(sessionManager.KEY_CONTRACT_ID)
        model.createdAt = datetime.now()
        model.modifiedAt = datetime.now()
        return model.register()


    @staticmethod
    def registerBasketAnalysisStore(model):
        model.contractId = sessionManager.getByKey(sessionManager.KEY_CONTRACT_ID)
        model.createdAt = datetime.now()
        model.modifiedAt = datetime.now()
        return model.register()


    @staticmethod
    def registerDailyBasketList(model):
        model.contractId = sessionManager.getByKey(sessionManager.KEY_CONTRACT_ID)
        model.createdAt = datetime.now()
        model.modifiedAt = datetime.now()
        return model.register()


    @staticmethod
    def getAnalysesByStoreIdAndSumDate(_storeId, _sumDate):
        result = db.session.query(BasketAnalysis)\
            .join(BasketAnalysisStore, BasketAnalysis.id == BasketAnalysisStore.basket_analysis_id)\
            .filter(
                BasketAnalysis.contract_id == sessionManager.getByKey(sessionManager.KEY_CONTRACT_ID),
                BasketAnalysisStore.store_id == _storeId, 
                db.func.date(BasketAnalysis.analysis_condition_date) == _sumDate
            ).all()
        return result


    @staticmethod
    def getDailyBasketListByStoreIdAndSumDate(_storeId, _sumDate):
        
        result = db.session.query(DailyBasketList)\
            .filter(
                DailyBasketList.contract_id == sessionManager.getByKey(sessionManager.KEY_CONTRACT_ID),
                DailyBasketList.store_id == _storeId, 
                db.func.date(DailyBasketList.target_date) == _sumDate
            ).all()
        return result


    @staticmethod
    def getDailyBasketListByStoreIdAndAnalysisConditionDateRange(_storeId: int, _analysisConditionDateFrom: str, _analysisConditionDateTo: str):
        """指定された期間のバスケット分析モデルを返します

        Arguments:
            _storeId {int} -- [description]
            _analysisConditionDateFrom {str} -- [description]
            _analysisConditionDateTo {str} -- [description]

        Returns:
            [type] -- [description]
        """
        result = db.session.query(DailyBasketList).filter(
            DailyBasketList.contract_id == sessionManager.getByKey(sessionManager.KEY_CONTRACT_ID),
            db.func.date(DailyBasketList.target_date) >= _analysisConditionDateFrom,
            db.func.date(DailyBasketList.target_date) <= _analysisConditionDateTo,
        ).all()
        return result 


    @staticmethod
    def getAnalysesByStoreIdAndAnalysisConditionDateRange(_storeId: int, _analysisConditionDateFrom: str, _analysisConditionDateTo: str):
        """指定された期間のバスケット分析モデルを返します

        Arguments:
            _storeId {int} -- [description]
            _analysisConditionDateFrom {str} -- [description]
            _analysisConditionDateTo {str} -- [description]

        Returns:
            [type] -- [description]
        """
        result = db.session.query(BasketAnalysis).filter(
            BasketAnalysis.contract_id == sessionManager.getByKey(sessionManager.KEY_CONTRACT_ID),
            db.func.date(BasketAnalysis.analysis_condition_date) >= _analysisConditionDateFrom,
            db.func.date(BasketAnalysis.analysis_condition_date) <= _analysisConditionDateTo,
        ).all()
        return result 