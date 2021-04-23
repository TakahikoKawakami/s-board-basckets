from app.common.abstracts.AbstractWebhook import AbstractWebhook
from app.domains.AccountDomainService import AccountDomainService
from app.domains.BasketDomainService import BasketDomainService

# from app.domains.TransactionsRepository import TransactionsRepository
# from app.domains.BasketAnalysesRepository import BasketAnalysesRepository

class TransactionsWebhook(AbstractWebhook):
    ACTION_CREATED = 'created'
    EVENT_GET_TRANSACTRION_DETAIL_LIST = 'get_transaction_detail_list'

    def __init__(self, loginAccount):
        super().__init__(loginAccount)
        

    async def received(self, event, body):
        self._logger.info('transaction webhook received.')
        self._logger.info('transactionHeadIds: ' + ','.join(body.get('transactionHeadIds')))
        
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
        
        urlList = body.get("file_url")
        if urlList is None:
            self._logger.info(body.get("message"))
            self._logger.info(f'request_code : "{body.get("request_code")}"')
            return
        basketDomainService = await BasketDomainService.createInstance(self._accessAccount)
        await basketDomainService.registerBasketByGzipUrlList(urlList)


    async def created(self, _targetTransactionHeadList):
        _basketDomainService = await BasketDomainService.createInstance(self._accessAccount)
        for _transactionHeadId in _targetTransactionHeadList:
            await _basketDomainService.registerBasketByTransactionHeadId(_transactionHeadId)

    def edited(self):
        pass

    def disposed(self):
        pass

    def canceled(self):
        pass