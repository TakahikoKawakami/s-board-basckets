from typing import cast, Dict
from app.common.abstracts.AbstractWebhook import AbstractWebhook
from app.domains.BasketDomainService import BasketDomainService


class TransactionsWebhook(AbstractWebhook):
    ACTION_CREATED = 'created'
    EVENT_GET_TRANSACTRION_DETAIL_LIST = 'get_transaction_detail_list'

    def __init__(self, login_account):
        super().__init__(login_account)

    async def received(self, event, body):
        self._logger.info('transaction webhook received.')
        self._logger.info(
            'transactionHeadIds: ' + ','.join(body.get('transactionHeadIds'))
        )

        if body['action'] == self.ACTION_CREATED:
            _targetTransactionHeadList = body['transactionHeadIds']
            await self.created(_targetTransactionHeadList)

    async def callback(self, event: str, body: dict):
        """取引明細CSV作成APIのcallback。csvからデータを取得し、daily_basket_list DBに登録します。

        Args:
            event (str): [description]
            body (dict): [description]
        """
        self._logger.info('transaction callback received.')

        url_list = body.get("file_url")
        if url_list is None:
            self._logger.info(body.get("message"))
            self._logger.info(f'request_code : "{body.get("request_code")}"')
            # データが0件だった場合、0件だったということがわかるよう、バスケットDBに空データを登録しておく
            if (body.get("message") == 'no data'):
                where_dict = cast(
                    Dict,
                    cast(
                        Dict,
                        body.get("state")
                    ).get("where")
                )
                store_id = where_dict["storeId"]
                target_date = where_dict["transactionDateTimeFrom"].\
                    split("T")[0]
                basket_domain_service = await BasketDomainService.\
                    create_instance(self._access_account)
                await basket_domain_service.register_empty_basket(
                    store_id,
                    target_date
                )
            return
        basket_domain_service = \
            await BasketDomainService.create_instance(self._access_account)
        await basket_domain_service.register_basket_by_gzip_url_list(url_list)

    async def created(self, _target_transaction_head_list):
        _basket_domain_service = await BasketDomainService.create_instance(self._access_account)
        for _transaction_head_id in _target_transaction_head_list:
            await _basket_domain_service.register_basket_by_transaction_head_id(_transaction_head_id)

    def edited(self):
        pass

    def disposed(self):
        pass

    def canceled(self):
        pass
