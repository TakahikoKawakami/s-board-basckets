from abc import ABC
from abc import abstractmethod

class AbstractBasket(ABC):
    @abstractmethod
    def append(self, transactionDetailList):
        pass


    @abstractmethod
    def analyze(self):
        pass


    @property
    @abstractmethod
    def result(self):
        pass

    
    @abstractmethod
    def salesRanking(self, top=1):
        pass