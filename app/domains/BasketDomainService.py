from typing import List, Dict
import json
import datetime

from app.common.utils import CsvUtil, EntityUtil, DictionaryUtil
from app.common.abstracts.AbstractDomainService import AbstractDomainService

from smaregipy.pos import TransactionDetailCollection

from app.entities.Baskets import Basket
from app.entities.Transactions import Transaction, TransactionHead, TransactionDetail
from app.entities.AssociationResult import AssociationResult
from app.entities.Fpgrowth import Fpgrowth
from app.models.DailyBasketList import DailyBasketList
from app.models import Store
from app.repositories import (
    TransactionsRepository,
    DailyBasketListRepository,
)
from app.factories import BasketsFactory


class BasketDomainService(AbstractDomainService):
    async def register_basket_by_transaction_head_id(
        self: 'BasketDomainService',
        transaction_head_id: int
    ) -> None:
        """取引ヘッダIDからバスケットデータを作成し、DBに登録します
        取引が存在しない場合でも、空のバスケットをDBに登録します

        Args:
            transactionHeadId (int): [description]
        """

        try:
            transaction = \
                await TransactionsRepository.get_by_id(transaction_head_id)
            basket = BasketsFactory.make_basket_by_transaction(transaction)

            daily_basket_list = \
                await DailyBasketListRepository.get_by_store_and_datetime(
                    store_id=basket.store_id,
                    datetime=basket.target_date
                )

            updated_basket_list = \
                await DailyBasketListRepository.append_basket_to(
                    daily_basket_list,
                    basket
                )

            self._logger.info('バスケットデータ登録完了')
            self._logger.info(repr(updated_basket_list))
        except Exception as e:
            self._logger.warning("!!raise exception!!")
            self._logger.warning(e)

    async def register_basket_by_transaction_list(
        self,
        transaction_list: List['Transaction']
    ) -> None:
        """取引entityリストからバスケットデータを作成し、DBに登録します

        Args:
            transactionList (list[Transaction]): [description]
        """
        self._logger.info("register basket by transaction list: start")
        daily_basket_list = None
        for transaction in transaction_list:
            self._logger.info(transaction.head.sum_date)
            _basket = Basket()
            _basket.set_by_transaction_head(transaction.head)
            _basket.set_by_transaction_detail_list(transaction.details)

            daily_basket_list_tuple = await DailyBasketList.get_or_create(
                contract_id=self.login_account.contract_id,
                store_id=_basket.store_id,
                target_date=_basket.target_date
            )

            daily_basket_list = daily_basket_list_tuple[0]  # [1]は取得したかのbool
            daily_basket_list.append_basket(_basket)
        if isinstance(daily_basket_list, DailyBasketList):
            await daily_basket_list.save()
        self._logger.info('バスケットデータ登録完了')
        self._logger.info(repr(daily_basket_list))
        self._logger.info("register basket by transaction list: finish")


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

    async def register_basket_by_gzip_url_list(
        self,
        url_list: List[str]
    ) -> None:
        """Gzip圧縮された取引明細データがおかれているurlリストから、バスケットデータを作成し、DBに登録します

        Args:
            urlList (list[str]): [description]
        """
        self._logger.info('データ取得開始---')
        transaction_detail_list_categorized_by_transaction_head_id = \
            self._get_transaction_detail_list_from_gzip_url_list(url_list)

        transaction_head_id_from = min(
            transaction_detail_list_categorized_by_transaction_head_id
            .keys()
        )
        transaction_head_id_to = max(
            transaction_detail_list_categorized_by_transaction_head_id
            .keys()
        )
        
        transaction_head_list = \
            await TransactionsRepository.get_head_list_by_id_range(
                head_id_from=transaction_head_id_from,
                head_id_to=transaction_head_id_to
            )
        self._logger.info(transaction_head_list)
        transaction_head_list_categorized_by_transaction_head_id = \
            EntityUtil.categorize_by_key(
                'transaction_head_id',
                transaction_head_list
            )

        self._logger.info('データ取得完了---')
        self._logger.info(
            '取引数: '
            + str(
                len(transaction_head_list_categorized_by_transaction_head_id)
            )
        )

        transaction_list = [
            Transaction.parse_obj({
                'head': transaction_head_list_categorized_by_transaction_head_id[head_id][0].dict(),
                'details': transaction_detail_list_categorized_by_transaction_head_id[head_id]
            }
            ) for head_id in transaction_head_list_categorized_by_transaction_head_id
        ]
        await self.register_basket_by_transaction_list(transaction_list)

    def _get_transaction_detail_list_from_gzip_url_list(
        self,
        url_list: List[str]
    ) -> Dict[int, List['TransactionDetail']]:
        """Gzip圧縮された取引明細ファイルをurlリストから順に取得し、取引ヘッダIDをキー、その明細リストを要素に持つ辞書を返します

        Returns:
            dict: 取引ヘッダID: [明細リスト] の辞書
        """
        transaction_detail_list = []
        for url in url_list:
            data_list = CsvUtil.get_gzip_data_from_url(url)
            snake_case_converted_list = [
                DictionaryUtil.convert_key_to_snake(data)
                for data in data_list
            ]
            transaction_detail_list.extend([
                TransactionDetail(**data)
                for data in snake_case_converted_list
            ])
        transaction_detail_list_categorized_by_transaction_head_id = \
            EntityUtil.categorize_by_key(
                'transaction_head_id',
                transaction_detail_list
            )
        return transaction_detail_list_categorized_by_transaction_head_id

    async def get_daily_basket_list_by_date_range(
        self,
        start_date: datetime.date,
        end_date: datetime.date
    ):
        account_setting = await self.login_account.account_setting_model
        store_id = account_setting.display_store_id

        _daily_basket_list = await DailyBasketList.filter(
            contract_id=self.login_account.contract_id,
            store_id=store_id,
            target_date__range=(start_date, end_date)
        ).all()
        return _daily_basket_list

    async def delete_daily_basket_list_by_date_range(
        self,
        start_date: datetime.date,
        end_date: datetime.date
    ):
        account_setting = await self.login_account.account_setting_model
        store_id = account_setting.display_store_id

        _daily_basket_list = await DailyBasketList.filter(
            contract_id=self.login_account.contract_id,
            store_id=store_id,
            target_date__range=(start_date, end_date)
        ).delete()
        return _daily_basket_list

    async def sync_daily_basket_list_by_date_range(
        self: 'BasketDomainService',
        start_date: datetime.datetime,
        end_date: datetime.datetime
    ) -> None:
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

        # _transactions_api = TransactionsApi()
        self._logger.info("send create_transaction_detail_csv api")
        where_dict = {
            'storeId': store_id,
            'transactionDateTimeFrom': start_date,
            'transactionDateTimeTo': end_date,
            'callbackUrl': (
                "{endpoint}/webhook"
                .format(endpoint=self._app_config.CALLBACK_URI)
            )
        }
        self._logger.debug("where_dict = " + json.dumps(where_dict))
        await (
            TransactionDetailCollection()
            .create_csv(
                sort={'sumDate': 'asc'},
                **where_dict
            )
        )
        # _transactions_api.create_transaction_detail_csv(
        #     where_dict=where_dict,
        #     sort='sumDate:asc'
        # )

        return

    async def register_empty_basket(
        self,
        store_id: int,
        target_date: datetime.datetime
    ) -> None:
        """空のバスケットデータを作成します
        もし存在していたら何もしない

        Args:
            storeId (int): [description]
            targetDate (datetime): [description]
        """
        daily_basket_list_tuple = await DailyBasketList.get_or_create(
            contract_id=self.login_account.contract_id,
            store_id=store_id,
            target_date=target_date
        )

        if daily_basket_list_tuple[1] is True:  # [1]は取得したか、作成したかのboolean
            # true: create
            _daily_basket_list = daily_basket_list_tuple[0]
            await _daily_basket_list.save()

    async def associate(
        self,
        target_store_id: str,
        target_date_from: datetime.datetime,
        target_date_to: datetime.datetime
    ) -> 'AssociationResult':
        store = await Store.filter(
            contract_id=self.login_account.contract_id,
            store_id=target_store_id
        ).first()
        if store is None:
            raise Exception("store does not exists")

        target_date_from_str = target_date_from.strftime("%Y-%m-%d")
        target_date_to_str = target_date_to.strftime("%Y-%m-%d")
        self._logger.info("-----search condition-----")
        self._logger.info("storeId     : " + target_store_id)
        self._logger.info("search_from : " + target_date_from_str)
        self._logger.info("search_to   : " + target_date_to_str)

        # 分析期間の日別バスケットリストを取得
        daily_basket_list_model_list = await DailyBasketList.filter(
            contract_id=self.login_account.contract_id,
            store_id=target_store_id,
            target_date__range=(target_date_from, target_date_to)
        )

        # 全データをマージ
        merged_basket_list = []
        for daily_basket_list_model in daily_basket_list_model_list:
            merged_basket_list += daily_basket_list_model.baskets

        # fpgrowthを用いて分析
        fpgrowth = Fpgrowth.create_by_data_list(
            merged_basket_list,
            0.1,
            self._logger
        )

        self._logger.debug("----- ----- vis.js created.")
        return vis
        association_result = AssociationResult(
            store=store,
            date_from=target_date_from,
            date_to=target_date_to,
            fpgrowth=fpgrowth
        )

        return association_result

    async def _convert_association_result_to_vis_js(self, fpgrowth):
        vis = None
        self._logger.info("-----convert association result to vis.js-----")
        self._logger.info(fpgrowth)
        if fpgrowth is not None:
            try:
                self._logger.debug("debug in if content")
                vis = fpgrowth.convertToVisJs()
                self._logger.debug("----- ----converted fpgrowth to vis.js-----")
                vis = await self._setVisNodeLabel(vis)
                self._logger.debug("----- ----set label for vis.js-----")
            except Exception as e:
                raise e
        
    async def _setVisNodeLabel(self, vis):
        productsApi = ProductsApi()
        result = VisJs()
        try:
            for node in vis.nodeList:
                product = await Product.filter(
                    contract_id = self._loginAccount.contractId,
                    product_id = node.id
                ).first()
                self._logger.debug(repr(product))

                if product is None:
                    self._logger.info("fetching product id: {}".format(node.id))
                    productByApi = productsApi.getProductById(node.id)
                    if productByApi is None:
                        self._logger.info("productsApi.getProductById is failed.")
                        node.label = "unknown"
                        result.nodeList.append(node)
                        continue
                    self._logger.debug(productByApi)
                    product = await Product.create(
                        contract_id = self._loginAccount.contractId,
                        product_id = productByApi['productId'],
                        name = productByApi['productName']
                        # color = productByApi['color'],
                        # size = productByApi['size'],
                        # price = productByApi['price']
                    )
                node.label = product.name
                result.nodeList.append(node)
        except Exception as e:
            self._logger.warning("!!raise exception!!")
            self._logger.warning(e)
            raise e

        result.edgeList = vis.edgeList
        return result
    
    async def convertAssociationResultToPickUpMessage(self, fpgrowth, storeId, dateFrom, dateTo):
        store = await self.target_store

        productFrom = None
        productTo = None
        if len(fpgrowth.result) > 0:
            productFromIdList = [result['id'] for result in fpgrowth.result[0]['from']]
            productToIdList = [result['id'] for result in fpgrowth.result[0]['to']]
            productFrom = await Product.filter(
                contract_id = self._loginAccount.contractId,
                product_id__in = productFromIdList
            ).all()
            productTo = await Product.filter(
                contract_id = self._loginAccount.contractId,
                product_id__in = productToIdList
            ).all()
        message = {
            'store': store,
            'from': dateFrom,
            'to': dateTo,
            'productFrom': productFrom,
            'productTo': productTo,
        }
        return message
