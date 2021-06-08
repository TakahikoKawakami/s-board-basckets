import datetime
import pytz
import json

from SmaregiPlatformApi.entities import TransactionHead, TransactionDetail

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
        self._input_data = []
        self._output = {}
        self._products = {}

        self._transaction_head_id = 0
        self._product_list = []  # {"id": xxx, "name": yyy}形式のdictリスト
        self._customer_group_id_list = []
        self._store_id = 0
        self._member_id = 0
        self._customer_sex_dict = {"male": 0, "female": 0, "unknown": 0}
        self._entry_date_division = ""  # 取引日時を２時間毎に区分わけ

        self._target_date = ""

        self._logger = logging.getLogger('flask.app')

    def __resp__(self):
        return "Basket entity<{}, {}, {}, {}, {}>".\
            format(
                self._product_list,
                self._customer_group_id_list,
                self._store_id,
                self._member_id,
                self._customer_sex_dict
            )

    def __str__(self):
        pass

    def set_by_transaction_detail_list(
        self,
        _transaction_detail_list: list['TransactionDetail']
    ) -> None:
        """取引明細からバスケットentityに必要なデータを抽出、セットします

        Arguments:
            transactionDetail {[type]} -- [description]
        """
        for transaction_detail in _transaction_detail_list:
            self._product_list.append(
                {
                    "id": transaction_detail.product_id,
                    "name": transaction_detail.product_name,
                    "categoryId": transaction_detail.category_id,
                }
            )

    def set_by_transaction_head(
        self,
        _transaction_head: 'TransactionHead'
    ) -> None:
        """取引ヘッダからバスケットentityに必要なデータを抽出、セットします

        Arguments:
            _transactionHead {[type]} -- [description]
        """
        self._transaction_head_id = _transaction_head.transaction_head_id

        if _transaction_head.sum_date is None:
            self._target_date = datetime.datetime.\
                now(pytz.timezone('Asia/Tokyo')).\
                strftime("%Y-%m-%d")
        else:
            self._target_date = _transaction_head.sum_date

        if _transaction_head.customer_id is not None:
            self._memberId = _transaction_head.customer_id
        else:
            self._memberId = "-1"

        if _transaction_head.customer_group_id is not None:
            self._customer_group_id_list.\
                append(_transaction_head.customer_group_id)
        for i in range(2, 6):
            if getattr(
                _transaction_head,
                "customer_group_id" + str(i)
            ) is not None:
                self._customer_group_id_list.append(
                    getattr(_transaction_head, "customer_group_id" + str(i))
                )

        self._store_id = _transaction_head.store_id

        if _transaction_head.guest_numbers_male is not None:
            self._customer_sex_dict["male"] = \
                _transaction_head.guest_numbers_male
        if _transaction_head.guest_numbers_female is not None:
            self._customer_sex_dict["female"] = \
                _transaction_head.guest_numbers_female
        if _transaction_head.guest_numbers_unknown is not None:
            self._customer_sex_dict["unknown"] = \
                _transaction_head.guest_numbers_unknown
        # TODO 取引日時区分

    def convert_list_for_analysis(self) -> list:
        """当entityをバスケット分析用のリスト型に変換します

        Returns:
            list -- [description]
        """
        result = []
        for product in self._product_list:
            result.append(self.PREFIXES_PRODUCT + json.dumps(product))

        if (
            "male" in self._customer_sex_dict and
            int(self._customer_sex_dict["male"]) != 0
        ):
            _customer_sex_dict = {}
            _customer_sex_dict["sex"] = "male"
            result.append(self.PREFIXES_SEX + json.dumps(_customer_sex_dict))
        if (
            "female" in self._customer_sex_dict and
            int(self._customer_sex_dict["female"]) != 0
        ):
            _customer_sex_dict = {}
            _customer_sex_dict["sex"] = "female"
            result.append(self.PREFIXES_SEX + json.dumps(_customer_sex_dict))
        if (
            "unknown" in self._customer_sex_dict and
            int(self._customer_sex_dict["unknown"]) != 0
        ):
            _customer_sex_dict = {}
            _customer_sex_dict["sex"] = "unknown"
            result.append(self.PREFIXES_SEX + json.dumps(_customer_sex_dict))
        if self._store_id != "":
            _store = {}
            _store['id'] = self._store_id
            result.append(self.PREFIXES_STORE + json.dumps(_store))

        if self._member_id != "":
            _member = {}
            _member['id'] = self._member_id
            result.append(self.PREFIXES_MEMBER + json.dumps(_member))

        if self._transaction_head_id != "":
            _transaction_head = {}
            _transaction_head['id'] = self._transaction_head_id
            result.append(
                self.PREFIXES_TRANSACTION_HEAD + json.dumps(_transaction_head)
            )

        return result

    @property
    def customer_group_id_list(self) -> list:
        return self._customer_group_id_list

    @customer_group_id_list.setter
    def customer_group_id_list(self, val: list) -> None:
        self._customer_group_id_list = val

    @property
    def store_id(self) -> int:
        return self._store_id

    @store_id.setter
    def store_id(self, val: int) -> None:
        self._store_id = val

    @property
    def member_id(self) -> int:
        return self._member_id

    @member_id.setter
    def member_id(self, val: int) -> None:
        self._member_id = val

    @property
    def customer_sex_dict(self) -> dict:
        return self._customer_sex_dict

    @customer_sex_dict.setter
    def customer_sex_dict(self, val: dict) -> None:
        self._customer_sex_dict = val

    @property
    def target_date(self):
        return self._target_date

    @target_date.setter
    def target_date(self, val):
        self._target_date = datetime.datetime.strptime(val, "%Y-%m-%d")
