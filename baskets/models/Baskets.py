from sqlalchemy import Column, Integer, Unicode, UnicodeText, ForeignKey, Boolean, DateTime, Enum, Text
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from pprint import pprint
import json

from database import db

import pyfpgrowth
import logging


class Basket(db.Model):
    """
    買い物かごモデル
    """
    __tablename__ = "baskets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Unicode(32), nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    analyze_result = Column(Text, nullable=False)
    analyze_condition = Column(Text)


    created_at = Column(DateTime)
    modified_at = Column(DateTime)


    def __init__(self):
        self._inputData = []
        self._output = {}
        self._products = {}

        self._productList = [] # {"id": xxx, "name": yyy}形式のdictリスト
        self._customerGroupIdList = []
        self._storeId = ""
        self._memberId = ""
        self._customerSexDict = {} # {"male": 1, "female": 2, "unknown": 3}
        self._entryDateDivision = "" # 取引日時を２時間毎に区分わけ

        self._logger = logging.getLogger('flask.app')
        
        
    def __resp__(self):
        return "Basket entity<{}, {}, {}, {}, {}>".format(self._productList, self._customerGroupId, self._storeId, self._memberId, self._customerSexDict)
        
        
    def __str__(self):
        pass
    
    
    def setByTransactionDetailList(self, _transactionDetailList)-> None:
        """取引明細からバスケットentityに必要なデータを抽出、セットします
        
        Arguments:
            transactionDetail {[type]} -- [description]
        """
        for transactionDetail in _transactionDetailList:
            self._productList.append(
                {
                    "id": transactionDetail['productId'],
                    "name": transactionDetail['productName'],
                    "categoryId": transactionDetail['categoryId'],
                }
            )
    

    def setByTransactionHead(self, _transactionHead) -> None:
        """取引ヘッダからバスケットentityに必要なデータを抽出、セットします

        Arguments:
            _transactionHead {[type]} -- [description]
        """
        if _transactionHead["customerId"] is not None:
            self._memberId = _transactionHead["customerId"]
        else:
            self._memberId = "非会員"
            
        if _transactionHead["customerGroupId"] is not None:
            self._customerGroupIdList.append(_transactionHead["customerGroupId"])
        for i in range(2,6):
            if _transactionHead["customerGroupId" + str(i)] is not None:
                self._customerGroupIdList.append(_transactionHead["customerGroupId" + str(i)])
                
        self._storeId = _transactionHead["storeId"]
        self._customerSexDict["male"] = _transactionHead["guestNumbersMale"]
        self._customerSexDict["female"] = _transactionHead["guestNumbersFemale"]
        self._customerSexDict["unknown"] = _transactionHead["guestNumbersUnknown"]
        # TODO 取引日時区分

    
    def convertListForAnalysis(self) -> list:
        """当entityをバスケット分析用のリスト型に変換します

        Returns:
            list -- [description]
        """
        result = []
        for product in self._productList:
            result.append("product__" + json.dumps(product))
        if "male" in self._customerSexDict and int(self._customerSexDict["male"]) != 0:
            result.append("customerSexMale")
        if "female" in self._customerSexDict and int(self._customerSexDict["female"]) != 0:
            result.append("customerSexFemale")
        if "unknown" in self._customerSexDict and int(self._customerSexDict["unknown"]) != 0:
            result.append("customerSexUnknown")
        if self._storeId != "":
            result.append("storeId:" + self._storeId)
        if self._memberId != "":
            result.append("memberId:" + self._memberId)
        
        return result
        

    @property
    def customerGroupIdList(self)->list:
        return self._customerGroupIdList


    @customerGroupIdList.setter
    def customerGroupIdList(self, val:list) -> None:
        self._customerGroupIdList = val

    
    @property
    def storeId(self)->int:
        return self._storeId


    @storeId.setter
    def storeId(self, val:int) -> None:
        self._storeId = val


    @property
    def memberId(self)->int:
        return self._memberId


    @memberId.setter
    def memberId(self, val:int) -> None:
        self._memberId = val


    @property
    def customerSexDict(self)->dict:
        return self._customerSexDict


    @customerSexDict.setter
    def customerSexDict(self, val:dict) -> None:
        self._customerSexDict = val


def MockBasket():
    pass