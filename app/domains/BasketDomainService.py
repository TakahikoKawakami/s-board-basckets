import logging
import datetime
import calendar

from app.common.utils import DictionaryUtil
import app.common.managers.SessionManager as sessionManager
from app.lib.Smaregi.API.POS.TransactionsApi import TransactionsApi

from app.common.abstracts.AbstractDomainService import AbstractDomainService
from app.entities.Baskets import Basket
from app.models.DailyBasketList import DailyBasketList
from app.models.Accounts import AccountSetting

class BasketDomainService(AbstractDomainService):
    def __init__(self, loginAccount):
        super().__init__(loginAccount)
        self.withSmaregiApi(loginAccount.accessToken.accessToken, loginAccount.contractId)

    async def registerBasketByTransactionHeadId(self, transactionHeadId):
        _transactionsApi = TransactionsApi(self._apiConfig)
        whereDict = {
            'with_details': 'all'
        }
        _apiResponse = _transactionsApi.getTransaction(transactionHeadId, whereDict=whereDict)
        _basket = Basket()
        _basket.setByTransactionHead(_apiResponse)
        _basket.setByTransactionDetailList(_apiResponse['details'])

        _dailyBasketListTuple = await DailyBasketList.get_or_create(
            contract_id = self._loginAccount.contractId,
            store_id = _basket.storeId,
            target_date = _basket.targetDate
        )

        _dailyBasketList = _dailyBasketListTuple[0] # [1]は取得したか、作成したかのboolean true: create
        _dailyBasketList.appendBasket(_basket)
        await _dailyBasketList.save()

    async def getDailyBasketListByDateRange(self, startDate: datetime.date, endDate: datetime.date):
        accountSetting = await self._loginAccount.accountSetting
        storeId = accountSetting.displayStoreId

        _dailyBasketList = await DailyBasketList.filter(
            contract_id = self._loginAccount.contractId,
            store_id = storeId,
            target_date__range = (startDate, endDate)
        ).all()
        return _dailyBasketList
    
    async def deleteDailyBasketListByDateRange(self, startDate: datetime.date, endDate: datetime.date):
        accountSetting = await self._loginAccount.accountSetting
        storeId = accountSetting.displayStoreId

        _dailyBasketList = await DailyBasketList.filter(
            contract_id = self._loginAccount.contractId,
            store_id = storeId,
            target_date__range = (startDate, endDate)
        ).delete()
        return _dailyBasketList

    async def syncDailyBasketListByDateRange(self, startDate: datetime.date, endDate: datetime.date):
        accountSetting = await self._loginAccount.accountSetting
        storeId = accountSetting.displayStoreId

        _transactionsApi = TransactionsApi(self._apiConfig)
        _targetTransactionHeadList = _transactionsApi.getTransactionHeadList(
            whereDict={
                'store_id': storeId,
                'sum_date-from': startDate,
                'sum_date-to': endDate,
            }, 
            sort='sumDate:asc'
        )
        # 締日ごとに並び替え
        _sumDateCategorizedTransactionHeadList = DictionaryUtil.categorizeByKey('sumDate', _targetTransactionHeadList)
        try:
            for _sumDate, _transactionHeadList in _sumDateCategorizedTransactionHeadList.items():
                # 締め日データが既にあれば無視。なければレコード作成
                _existedRecords = await DailyBasketList.filter(
                    contract_id = self._loginAccount.contractId,
                    store_id = storeId,
                    target_date = _sumDate
                ).all()
                if (_existedRecords == []):

                    _dailyBasketListModelList = self._getBasketListByTransactionHeadList(_transactionHeadList, _sumDate)
                    for _dailyBasketListModel in _dailyBasketListModelList:
                        await _dailyBasketListModel.save()
                        # self._logger.debug(_registered)
        except Exception as e:
            raise e

        _result = await DailyBasketList.filter(
            contract_id = self._loginAccount.contractId,
            store_id = storeId,
            target_date__range = (startDate, endDate)
        ).all()
        return _result 


        _dailyBasketList = await DailyBasketList.filter(
            contract_id = self._loginAccount.contractId,
            store_id = storeId,
            target_date__range = (startDate, endDate)
        ).delete()
        return _dailyBasketList

    def _getBasketListByTransactionHeadList(self, _transactionHeadList, _sumDate):
        """取引ヘッダリストに紐づく全取引明細を取得し、日別バスケット分析用データモデルを返却します

        Arguments:
            _transactionHeadList {TransactionHead} -- APIで取得した取引ヘッダリスト
            _sumDate {str} -- 締め日（Y-m-d）

        Returns:
            BasketAnalysis -- バスケット分析モデル（分析済）
        """
        
        _transactionsApi = TransactionsApi(self._apiConfig)
        _dailyBasketListDict = {}
        for _transactionHead in _transactionHeadList:
            _transactionDetailList = _transactionsApi.getTransactionDetail(_transactionHead['transactionHeadId'])
            _basketModel = Basket()
            _basketModel.setByTransactionHead(_transactionHead)
            _basketModel.setByTransactionDetailList(_transactionDetailList)

            if (_basketModel.storeId not in _dailyBasketListDict.keys()):
                _dailyBasketListDict[_basketModel.storeId] = []

            _dailyBasketListDict[_basketModel.storeId].append(_basketModel)
            
        _resultList = []
        for _storeId, _dailyBasketList in _dailyBasketListDict.items():
            _dailyBasketListModel = DailyBasketList()
            _dailyBasketListModel.contractId = self._loginAccount.contractId
            _dailyBasketListModel.basketList = _dailyBasketList
            _dailyBasketListModel.storeId = _storeId
            _dailyBasketListModel.targetDate = datetime.datetime.strptime(_sumDate, "%Y-%m-%d")
            _resultList.append(_dailyBasketListModel)
            
        return _resultList