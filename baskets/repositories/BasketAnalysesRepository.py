import common.managers.SessionManager as sessionManager
from datetime import datetime
from baskets.models.BasketAnalyses import BasketAnalysis
from baskets.models.BasketAnalysisConditions import BasketAnalysisCondition
from baskets.models.BasketAnalysisStores import BasketAnalysisStore
from database import db

class BasketAnalysesRepository():
    def __init__(self, modelFactory):
        self._modelFactory = modelFactory


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
    def commit():
        db.session.commit()
        

    @staticmethod
    def rollback():
        db.session.rollback()
    

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