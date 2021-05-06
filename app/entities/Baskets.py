import datetime
import pytz
from pprint import pprint
import json

import app.database as db
from app.lib.Smaregi.API.POS.entities import TransactionHead, TransactionDetail

import logging


class Basket():
    """
    買い物かごentity
    """
    PREFIXES_TRANSACTION_HEAD = "transactionHead__"
    PREFIXES_PRODUCT = "product__"
    PREFIXES_SEX = "customerSex__"
    PREFIXES_STORE = "store__"
    PREFIXES_MEMBER = "member__"


    def __init__(self):
        self._inputData = []
        self._output = {}
        self._products = {}

        self._transactionHeadId = ""
        self._productList = [] # {"id": xxx, "name": yyy}形式のdictリスト
        self._customerGroupIdList = []
        self._storeId = ""
        self._memberId = ""
        self._customerSexDict = {"male": 0, "female": 0, "unknown": 0}
        self._entryDateDivision = "" # 取引日時を２時間毎に区分わけ

        self._targetDate = ""

        self._logger = logging.getLogger('flask.app')
        
        
    def __resp__(self):
        return "Basket entity<{}, {}, {}, {}, {}>".format(self._productList, self._customerGroupId, self._storeId, self._memberId, self._customerSexDict)
        
        
    def __str__(self):
        pass
    
    
    def setByTransactionDetailList(self, _transactionDetailList: list['TransactionDetail'])-> None:
        """取引明細からバスケットentityに必要なデータを抽出、セットします
        
        Arguments:
            transactionDetail {[type]} -- [description]
        """
        for transactionDetail in _transactionDetailList:
            self._productList.append(
                {
                    "id": transactionDetail.productId,
                    "name": transactionDetail.productName,
                    "categoryId": transactionDetail.categoryId,
                }
            )
    

    def setByTransactionHead(self, _transactionHead: 'TransactionHead') -> None:
        """取引ヘッダからバスケットentityに必要なデータを抽出、セットします

        Arguments:
            _transactionHead {[type]} -- [description]
        """
        self._transactionHeadId = _transactionHead.transactionHeadId

        if _transactionHead.sumDate is None:
            self._targetDate = datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime("%Y-%m-%d")
        else:
            self._targetDate = _transactionHead.sumDate

        if _transactionHead.customerId is not None:
            self._memberId = _transactionHead.customerId
        else:
            self._memberId = "-1"
            
        if _transactionHead.customerGroupId is not None:
            self._customerGroupIdList.append(_transactionHead.customerGroupId)
        for i in range(2,6):
            if getattr(_transactionHead, "customerGroupId" + str(i)) is not None:
                self._customerGroupIdList.append(getattr(_transactionHead, "customerGroupId" + str(i)))
                
        self._storeId = _transactionHead.storeId
        
        if _transactionHead.guestNumbersMale is not None:
            self._customerSexDict["male"] = _transactionHead.guestNumbersMale
        if _transactionHead.guestNumbersFemale is not None:
            self._customerSexDict["female"] = _transactionHead.guestNumbersFemale
        if _transactionHead.guestNumbersUnknown is not None:
            self._customerSexDict["unknown"] = _transactionHead.guestNumbersUnknown
        # TODO 取引日時区分

    
    def convertListForAnalysis(self) -> list:
        """当entityをバスケット分析用のリスト型に変換します

        Returns:
            list -- [description]
        """
        result = []
        for product in self._productList:
            result.append(self.PREFIXES_PRODUCT + json.dumps(product))

        if "male" in self._customerSexDict and int(self._customerSexDict["male"]) != 0:
            _customerSexDict = {}
            _customerSexDict["sex"] = "male"
            result.append(self.PREFIXES_SEX + json.dumps(_customerSexDict))
        if "female" in self._customerSexDict and int(self._customerSexDict["female"]) != 0:
            _customerSexDict = {}
            _customerSexDict["sex"] = "female"
            result.append(self.PREFIXES_SEX + json.dumps(_customerSexDict))
        if "unknown" in self._customerSexDict and int(self._customerSexDict["unknown"]) != 0:
            _customerSexDict = {}
            _customerSexDict["sex"] = "unknown"
            result.append(self.PREFIXES_SEX + json.dumps(_customerSexDict))
        if self._storeId != "":
            _store = {}
            _store['id'] = self._storeId
            result.append(self.PREFIXES_STORE + json.dumps(_store))

        if self._memberId != "":
            _member = {}
            _member['id'] = self._memberId
            result.append(self.PREFIXES_MEMBER + json.dumps(_member))

        if self._transactionHeadId != "":
            _transactionHead = {}
            _transactionHead['id'] = self._transactionHeadId
            result.append(self.PREFIXES_TRANSACTION_HEAD + json.dumps(_transactionHead))
        
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

    @property
    def targetDate(self):
        return self._targetDate

    @targetDate.setter
    def targetDate(self, val):
        self._targetDate = datetime.datetime.strptime(val, "%Y-%m-%d")
