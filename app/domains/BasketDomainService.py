import logging
import datetime
import calendar

from app.common.utils import CsvUtil, DictionaryUtil, EntityUtil
import app.common.managers.SessionManager as sessionManager

from app.entities.Transactions import Transaction
from app.lib.Smaregi.API.POS.TransactionsApi import TransactionsApi
from app.lib.Smaregi.API.POS.entities import TransactionHead, TransactionDetail


from app.common.abstracts.AbstractDomainService import AbstractDomainService
from app.entities.Baskets import Basket
from app.entities.Transactions import Transaction
from app.models.DailyBasketList import DailyBasketList
from app.models.Accounts import AccountSetting

class BasketDomainService(AbstractDomainService):
    def __init__(self, loginAccount):
        super().__init__(loginAccount)
        self.withSmaregiApi(loginAccount.accessToken.accessToken, loginAccount.contractId)

    async def registerBasketByTransactionHeadId(self, transactionHeadId: int) -> None:
        """取引ヘッダIDからバスケットデータを作成し、DBに登録します

        Args:
            transactionHeadId (int): [description]
        """

        _transactionsApi = TransactionsApi(self._apiConfig)
        whereDict = {
            'with_details': 'all'
        }
        try:
            _apiResponse = _transactionsApi.getTransaction(transactionHeadId, whereDict=whereDict)
            transaction = Transaction(_apiResponse['head'], _apiResponse['details'])
            _basket = Basket()
            _basket.setByTransactionHead(transaction.head)
            _basket.setByTransactionDetailList(transaction.details)

            _dailyBasketListTuple = await DailyBasketList.get_or_create(
                contract_id = self._loginAccount.contractId,
                store_id = _basket.storeId,
                target_date = _basket.targetDate
            )

            _dailyBasketList = _dailyBasketListTuple[0] # [1]は取得したか、作成したかのboolean true: create
            _dailyBasketList.appendBasket(_basket)
            await _dailyBasketList.save()
            self._logger.info('バスケットデータ登録完了')
            self._logger.info(repr(_dailyBasketList))
        except Exception as e:
            self._logger.warning("!!raise exception!!")
            self._logger.warning(e)


    async def registerBasketByTransactionList(self, transactionList: list['Transaction']) -> None:
        """取引entityリストからバスケットデータを作成し、DBに登録します

        Args:
            transactionList (list[Transaction]): [description]
        """
        for transaction in transactionList:
            _basket = Basket()
            _basket.setByTransactionHead(transaction.head)
            _basket.setByTransactionDetailList(transaction.details)

            _dailyBasketListTuple = await DailyBasketList.get_or_create(
                contract_id = self._loginAccount.contractId,
                store_id = _basket.storeId,
                target_date = _basket.targetDate
            )

            _dailyBasketList = _dailyBasketListTuple[0] # [1]は取得したか、作成したかのboolean true: create
            _dailyBasketList.appendBasket(_basket)
        await _dailyBasketList.save()
        self._logger.info('バスケットデータ登録完了')
        self._logger.info(repr(_dailyBasketList))


    async def registerBasketByTransaction(self, transactionHead, transactionDetail):
        _basket = Basket()
        _basket.setByTransactionHead(transactionHead)
        _basket.setByTransactionDetailList(transactionDetail)

        _dailyBasketListTuple = await DailyBasketList.get_or_create(
            contract_id = self._loginAccount.contractId,
            store_id = _basket.storeId,
            target_date = _basket.targetDate
        )

        _dailyBasketList = _dailyBasketListTuple[0] # [1]は取得したか、作成したかのboolean true: create
        _dailyBasketList.appendBasket(_basket)
        await _dailyBasketList.save()
        self._logger.info('バスケットデータ登録完了')
        self._logger.info(repr(_dailyBasketList))


    async def registerBasketByGzipUrlList(self, urlList: list[str]) -> None:
        """Gzip圧縮された取引明細データがおかれているurlリストから、バスケットデータを作成し、DBに登録します

        Args:
            urlList (list[str]): [description]
        """
        self._logger.info('データ取得開始---')
        transactionDetailListCategorizedByTransactionHeadId = self._getTransactionDetailListFromGzipUrlList(urlList)

        transactionHeadIdFrom = min(transactionDetailListCategorizedByTransactionHeadId.keys())
        transactionHeadIdTo = max(transactionDetailListCategorizedByTransactionHeadId.keys())
        
        transactionHeadListCategorizedByTransactionHeadId = self._getTransactionHeadListByAPI(headIdFrom = transactionHeadIdFrom, headIdTo = transactionHeadIdTo)

        self._logger.info('データ取得完了---')
        self._logger.info('取引数: ' + str(len(transactionHeadListCategorizedByTransactionHeadId)))

        transactionList = [
            Transaction(
                transactionHeadListCategorizedByTransactionHeadId[headId][0],
                transactionDetailListCategorizedByTransactionHeadId[headId]
            ) for headId in transactionHeadListCategorizedByTransactionHeadId.keys()
        ]
        await self.registerBasketByTransactionList(transactionList)


    def _getTransactionDetailListFromGzipUrlList(self, urlList: list[str]) -> dict[int, list['TransactionDetail']]:
        """Gzip圧縮された取引明細ファイルをurlリストから順に取得し、取引ヘッダIDをキー、その明細リストを要素に持つ辞書を返します

        Returns:
            dict: 取引ヘッダID: [明細リスト] の辞書
        """
        transactionDetailList = []
        for url in urlList:
            dataList = CsvUtil.getGzipDataFromUrl(url)
            transactionDetailList.extend([TransactionDetail(data) for data in dataList])
        transactionDetailListCategorizedByTransactionHeadId = EntityUtil.categorizeByKey('transactionHeadId', transactionDetailList)
        return transactionDetailListCategorizedByTransactionHeadId


    def _getTransactionHeadListByAPI(self, headIdFrom: int, headIdTo: int) -> dict[int, list[TransactionHead]]:
        """APIから取引ヘッダリストを取得します

        Args:
            headIdFrom (int): [description]
            headIdTo (int): [description]

        Returns:
            dict: 取引ヘッダID: [ヘッダリスト] の辞書
        """
        transactionsApi = TransactionsApi(self._apiConfig)
        transactionHeadList = transactionsApi.getTransactionHeadList(whereDict= {
            'transaction_head_id-from': headIdFrom,
            'transaction_head_id-to': headIdTo,
        })
        transactionHeadListCategorizedByTransactionHeadId = EntityUtil.categorizeByKey('transactionHeadId', transactionHeadList)
        return transactionHeadListCategorizedByTransactionHeadId


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


    async def syncDailyBasketListByDateRange(self, startDate: datetime.datetime, endDate: datetime.datetime):
        """指定された期間の日次バスケットデータを作成、同期します

        Args:
            startDate (datetime.datetime): 開始日
            endDate (datetime.datetime): 終了日

        Raises:
            e: [description]

        Returns:
            [type]: [description]
        """
        accountSetting = await self._loginAccount.accountSetting
        storeId = accountSetting.displayStoreId

        _transactionsApi = TransactionsApi(self._apiConfig)
        _transactionsApi.createTransactionDetailCsv(
            whereDict={
                'storeId': storeId,
                'transactionDateTimeFrom': startDate,
                'transactionDateTimeTo': endDate,
                'callbackUrl': self._appConfig.CALLBACK_URI + '/webhook'
            }, 
            sort='sumDate:asc'
        )

        # _targetTransactionHeadList = _transactionsApi.getTransactionHeadList(
        #     whereDict={
        #         'store_id': storeId,
        #         'sum_date-from': startDate,
        #         'sum_date-to': endDate,
        #     }, 
        #     sort='sumDate:asc'
        # )
        # # 締日ごとに並び替え
        # _sumDateCategorizedTransactionHeadList = DictionaryUtil.categorizeByKey('sumDate', _targetTransactionHeadList)
        # try:
        #     for _sumDate, _transactionHeadList in _sumDateCategorizedTransactionHeadList.items():
        #         # 締め日データが既にあれば無視。なければレコード作成
        #         _existedRecords = await DailyBasketList.filter(
        #             contract_id = self._loginAccount.contractId,
        #             store_id = storeId,
        #             target_date = _sumDate
        #         ).all()
        #         if (_existedRecords == []):

        #             _dailyBasketListModelList = self._getBasketListByTransactionHeadList(_transactionHeadList, _sumDate)
        #             for _dailyBasketListModel in _dailyBasketListModelList:
        #                 await _dailyBasketListModel.save()
        #                 # self._logger.debug(_registered)
        # except Exception as e:
        #     raise e

        # _result = await DailyBasketList.filter(
        #     contract_id = self._loginAccount.contractId,
        #     store_id = storeId,
        #     target_date__range = (startDate, endDate)
        # ).all()
        # return _result 


        # _dailyBasketList = await DailyBasketList.filter(
        #     contract_id = self._loginAccount.contractId,
        #     store_id = storeId,
        #     target_date__range = (startDate, endDate)
        # ).delete()
        # return _dailyBasketList
        return

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