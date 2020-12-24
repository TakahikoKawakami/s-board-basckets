from flask import session
from datetime import datetime
from baskets.models.BasketAnalyses import BasketAnalysis
from baskets.models.BasketAnalysisConditions import BasketAnalysisCondition
from database import db

class BasketAnalysesRepository():
    def __init__(self, modelFactory):
       self._modelFactory = modelFactory


    @staticmethod
    def registerBasketAnalysis(model):
        model.contractId = session['contract_id']
        model.createdAt = datetime.now()
        model.modifiedAt = datetime.now()
        return model.register()


    @staticmethod
    def registerBasketAnalysisStore(model):
        model.contractId = session['contract_id']
        model.createdAt = datetime.now()
        model.modifiedAt = datetime.now()
        return model.register()


    @staticmethod
    def commit():
        db.session.commit()
        

    @staticmethod
    def rollback():
        db.session.rollback()