from models.Accounts import Account, MockAccount
from models.BasketAnalyses import BasketAnalysis
from models.BasketAnalysisConditions import BasketAnalysisCondition
from models.DailyBasketList import DailyBasketList


class ModelFactory():
    def __init__(self, appConfig):
        self._appConfig = appConfig


    def createAccount(self):
        if   (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_PRODUCTION):
            return Account()
        elif (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_STAGING):
            return Account()
        elif (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_LOCAL):
            return Account()
        elif (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_MOCK):
            return MockAccount()


    def createBasketAnalysis(self):
        if   (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_PRODUCTION):
            return BasketAnalysis()
        elif (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_STAGING):
            return BasketAnalysis()
        elif (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_LOCAL):
            return BasketAnalysis()
        elif (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_MOCK):
            return BasketAnalysis()


    def createBasketAnalysisCondition(self):
        if   (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_PRODUCTION):
            return BasketAnalysisCondition()
        elif (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_STAGING):
            return BasketAnalysisCondition()
        elif (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_LOCAL):
            return BasketAnalysisCondition()
        elif (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_MOCK):
            return BasketAnalysisCondition()


    def createDailyBasketList(self):
        if   (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_PRODUCTION):
            return DailyBasketList()
        elif (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_STAGING):
            return DailyBasketList()
        elif (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_LOCAL):
            return DailyBasketList()
        elif (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_MOCK):
            return DailyBasketList()