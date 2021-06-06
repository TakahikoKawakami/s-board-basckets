import json
import datetime

from app.common.utils import CsvUtil,  EntityUtil

from app.entities.Transactions import Transaction
from SmaregiPlatformApi.pos import TransactionsApi
from SmaregiPlatformApi.entities import TransactionHead, TransactionDetail


from app.common.abstracts.AbstractDomainService import AbstractDomainService
from app.entities.Baskets import Basket
from app.entities.Transactions import Transaction
from app.models.DailyBasketList import DailyBasketList


class BasketDomainService(AbstractDomainService):
    def __init__(self, login_account):
        super().__init__(login_account)
        self.with_smaregi_api(login_account.access_token_entity.access_token, login_account.contract_id)

    async def register_basket_by_transaction_head_id(self, transaction_head_id: int) -> None:
        """取引ヘッダIDからバスケットデータを作成し、DBに登録します
        取引が存在しない場合でも、空のバスケットをDBに登録します

        Args:
            transactionHeadId (int): [description]
        """

        _transactions_api = TransactionsApi(self._api_config)
        where_dict = {
            'with_details': 'all'
        }
        try:
            _api_response = _transactions_api.get_transaction(transaction_head_id, where_dict=where_dict)
            transaction = Transaction(_api_response['head'], _api_response['details'])
            _basket = Basket()
            _basket.set_by_transaction_head(transaction.head)
            _basket.set_by_transaction_detail_list(transaction.details)

            _daily_basket_list_tuple = await DailyBasketList.get_or_create(
                contract_id=self.login_account.contract_id,
                store_id=_basket.store_id,
                target_date=_basket.target_date
            )

            _daily_basket_list = _daily_basket_list_tuple[0]  # [1]は取得したか、作成したかのboolean true: create
            _daily_basket_list.appendBasket(_basket)
            await _daily_basket_list.save()
            self._logger.info('バスケットデータ登録完了')
            self._logger.info(repr(_daily_basket_list))
        except Exception as e:
            self._logger.warning("!!raise exception!!")
            self._logger.warning(e)


    async def register_basket_by_transaction_list(self, transaction_list: list['Transaction']) -> None:
        """取引entityリストからバスケットデータを作成し、DBに登録します

        Args:
            transactionList (list[Transaction]): [description]
        """
        for transaction in transaction_list:
            _basket = Basket()
            _basket.set_by_transaction_head(transaction.head)
            _basket.set_by_transaction_detail_list(transaction.details)

            _daily_basket_list_tuple = await DailyBasketList.get_or_create(
                contract_id=self.login_account.contract_id,
                store_id=_basket.store_id,
                target_date=_basket.target_date
            )

            _daily_basket_list = _daily_basket_list_tuple[0] # [1]は取得したか、作成したかのboolean true: create
            _daily_basket_list.appendBasket(_basket)
        await _daily_basket_list.save()
        self._logger.info('バスケットデータ登録完了')
        self._logger.info(repr(_daily_basket_list))


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


    async def register_basket_by_gzip_url_list(self, url_list: list[str]) -> None:
        """Gzip圧縮された取引明細データがおかれているurlリストから、バスケットデータを作成し、DBに登録します

        Args:
            urlList (list[str]): [description]
        """
        self._logger.info('データ取得開始---')
        transaction_detail_list_categorized_by_transaction_head_id = self._get_transaction_detail_list_from_gzip_url_list(url_list)

        transaction_head_id_from = min(transaction_detail_list_categorized_by_transaction_head_id.keys())
        transaction_head_id_to = max(transaction_detail_list_categorized_by_transaction_head_id.keys())
        
        transaction_head_list_categorized_by_transaction_head_id = self._get_transaction_head_list_by_api(head_id_from=transaction_head_id_from, head_id_to=transaction_head_id_to)

        self._logger.info('データ取得完了---')
        self._logger.info('取引数: ' + str(len(transaction_head_list_categorized_by_transaction_head_id)))

        transaction_list = [
            Transaction(
                transaction_head_list_categorized_by_transaction_head_id[head_id][0],
                transaction_detail_list_categorized_by_transaction_head_id[head_id]
            ) for head_id in transaction_head_list_categorized_by_transaction_head_id.keys()
        ]
        await self.register_basket_by_transaction_list(transaction_list)


    def _get_transaction_detail_list_from_gzip_url_list(self, url_list: list[str]) -> dict[int, list['TransactionDetail']]:
        """Gzip圧縮された取引明細ファイルをurlリストから順に取得し、取引ヘッダIDをキー、その明細リストを要素に持つ辞書を返します

        Returns:
            dict: 取引ヘッダID: [明細リスト] の辞書
        """
        transaction_detail_list = []
        for url in url_list:
            data_list = CsvUtil.get_gzip_data_from_url(url)
            transaction_detail_list.extend([TransactionDetail(data) for data in data_list])
        transaction_detail_list_categorized_by_transaction_head_id = EntityUtil.categorize_by_key('transaction_head_id', transaction_detail_list)
        return transaction_detail_list_categorized_by_transaction_head_id

    def _get_transaction_head_list_by_api(self, head_id_from: int, head_id_to: int) -> dict[int, list[TransactionHead]]:
        """APIから取引ヘッダリストを取得します

        Args:
            headIdFrom (int): [description]
            headIdTo (int): [description]

        Returns:
            dict: 取引ヘッダID: [ヘッダリスト] の辞書
        """
        transactions_api = TransactionsApi(self._api_config)
        transaction_head_list = transactions_api.get_transaction_head_list(where_dict= {
            'transaction_head_id-from': head_id_from,
            'transaction_head_id-to': head_id_to,
        })
        transaction_head_list_categorized_by_transaction_head_id = EntityUtil.categorize_by_key('transaction_head_id', transaction_head_list)
        return transaction_head_list_categorized_by_transaction_head_id


    async def get_daily_basket_list_by_date_range(self, start_date: datetime.date, end_date: datetime.date):
        account_setting = await self.login_account.account_setting_model
        store_id = account_setting.display_store_id

        _daily_basket_list = await DailyBasketList.filter(
            contract_id=self.login_account.contract_id,
            store_id=store_id,
            target_date__range=(start_date, end_date)
        ).all()
        return _daily_basket_list
    

    async def delete_daily_basket_list_by_date_range(self, start_date: datetime.date, end_date: datetime.date):
        account_setting = await self.login_account.account_setting_model
        store_id = account_setting.display_store_id

        _daily_basket_list = await DailyBasketList.filter(
            contract_id=self.login_account.contract_id,
            store_id=store_id,
            target_date__range=(start_date, end_date)
        ).delete()
        return _daily_basket_list

    async def sync_daily_basket_list_by_date_range(self, start_date: datetime.datetime, end_date: datetime.datetime):
        """指定された期間の日次バスケットデータを作成、同期します

        Args:
            startDate (datetime.datetime): 開始日
            endDate (datetime.datetime): 終了日

        Raises:
            e: [description]

        Returns:
            [type]: [description]
        """
        account_setting = await self.login_account.account_setting_model
        store_id = account_setting.display_store_id
        if store_id is None:
            self._logger.info("store_id is None")
            raise Exception("store_id is None")

        _transactions_api = TransactionsApi(self._api_config)
        self._logger.info("send create_transaction_detail_csv api")
        where_dict = {
            'storeId': store_id,
            'transactionDateTimeFrom': start_date,
            'transactionDateTimeTo': end_date,
            'callbackUrl': self._app_config.CALLBACK_URI + '/webhook'
        }
        self._logger.debug("where_dict = " + json.dumps(where_dict))
        _transactions_api.create_transaction_detail_csv(
            where_dict=where_dict,
            sort='sumDate:asc'
        )

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

    async def register_empty_basket(self, store_id: int, target_date: datetime.datetime) -> None:
        """空のバスケットデータを作成します
        もし存在していたら何もしない

        Args:
            storeId (int): [description]
            targetDate (datetime): [description]
        """
        import pdb; pdb.set_trace()
        daily_basket_list_tuple = await DailyBasketList.get_or_create(
            contract_id=self.login_account.contract_id,
            store_id=store_id,
            target_date=target_date
        )

        if daily_basket_list_tuple[1] is True:  # [1]は取得したか、作成したかのboolean true: create
            _daily_basket_list = daily_basket_list_tuple[0]
            await _daily_basket_list.save()
