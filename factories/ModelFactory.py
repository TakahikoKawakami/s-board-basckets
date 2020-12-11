
from baskets.models.Baskets import Basket, MockBasket


class ModelFactory():
    def __init__(self, appConfig):
        self._appConfig = appConfig


    def createBasket(self):
        if   (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_PRODUCTION):
            return Basket()
        elif (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_STAGING):
            return Basket()
        elif (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_LOCAL):
            return Basket()
        elif (self._appConfig.ENV_DIVISION == self._appConfig.ENV_DIVISION_MOCK):
            return MockBasket()
