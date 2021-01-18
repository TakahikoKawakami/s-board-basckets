import common.managers.SessionManager as sessionManager
from common.abstracts.AbstractRepository import AbstractRepository
import datetime
from models.DailyBasketList import DailyBasketList
from models.BasketAnalyses import BasketAnalysis
import database as db
from common.utils import DictionaryUtil
from entities.Baskets import Basket
import logging

from lib.Smaregi.API.POS.TransactionsApi import TransactionsApi

class BasketAnalysesRepository(AbstractRepository):
    def __init__(self):
        super().__init__()

        self._logger = logging.getLogger('flask.app')


    @staticmethod
    def registerBasketAnalysis(model):
        model.contractId = sessionManager.getByKey(sessionManager.KEY_CONTRACT_ID)
        model.createdAt = datetime.datetime.now()
        model.modifiedAt = datetime.datetime.now()
        return model.register()


    @staticmethod
    def registerBasketAnalysisStore(model):
        model.contractId = sessionManager.getByKey(sessionManager.KEY_CONTRACT_ID)
        model.createdAt = datetime.datetime.now()
        model.modifiedAt = datetime.datetime.now()
        return model.register()


    @staticmethod
    def registerDailyBasketList(model):
        model.contractId = sessionManager.getByKey(sessionManager.KEY_CONTRACT_ID)
        model.createdAt = datetime.datetime.now()
        model.modifiedAt = datetime.datetime.now()
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


    def getDailyBasketListByStoreIdAndAnalysisDateRange(self, _storeId: int, _dateFrom: str, _dateTo: str):
        """指定された期間のバスケット分析モデルを返します

        Arguments:
            _storeId {int} -- [description]
            _analysisConditionDateFrom {str} -- [description]
            _analysisConditionDateTo {str} -- [description]

        Returns:
            [type] -- [description]
        """
        _transactionsApi = TransactionsApi(self._apiConfig)
        _targetTransactionHeadList = _transactionsApi.getTransactionHeadList(
            whereDict={
                'store_id': _storeId,
                'sum_date-from': _dateFrom,
                'sum_date-to': _dateTo,
            }, 
            sort='sumDate:asc'
        )
        # 締日ごとに並び替え
        _sumDateCategorizedTransactionHeadList = DictionaryUtil.categorizeByKey('sumDate', _targetTransactionHeadList)
        self._logger.debug("-----categorized transaction head list-----")
        # self._logger.debug(_sumDateCategorizedTransactionHeadList)

        # 分析期間に該当する取引をDBから取得
        # ループでまわし、分析用データを作成する
        # DBにない日付の場合、該当日付の取引をAPIで取得、DBに保存
        # 対象取引データを取得
        # 取得したヘッダを締め日付ごとにみていく
        try:
            _basketAnalysis = BasketAnalysis()
            for _sumDate, _transactionHeadList in _sumDateCategorizedTransactionHeadList.items():
                # 締め日データが既にあれば無視。なければレコード作成
                _existedRecords = self.getDailyBasketListByStoreIdAndSumDate(_storeId, _sumDate)
                if (_existedRecords == []):
                    self._logger.debug("-----register basket analysis-----")

                    _dailyBasketListModelList = self.getBasketListByTransactionHeadList(_transactionHeadList, _sumDate)
                    for _dailyBasketListModel in _dailyBasketListModelList:
                        _registered = self.registerDailyBasketList(_dailyBasketListModel)
                        # self._logger.debug(_registered)
                
            self.commit()
        except Exception as e:
            self.rollback()
            self._logger.debug("raise error -----")
            raise e


        _result = db.session.query(DailyBasketList).filter(
            DailyBasketList.contract_id == sessionManager.getByKey(sessionManager.KEY_CONTRACT_ID),
            db.func.date(DailyBasketList.target_date) >= _dateFrom,
            db.func.date(DailyBasketList.target_date) <= _dateTo,
        ).all()
        return _result 


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


    def getBasketListByTransactionHeadList(self, _transactionHeadList, _sumDate):
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
            _dailyBasketListModel.basketList = _dailyBasketList
            _dailyBasketListModel.storeId = _storeId
            _dailyBasketListModel.targetDate = datetime.datetime.strptime(_sumDate, "%Y-%m-%d")
            _resultList.append(_dailyBasketListModel)
            
        return _resultList