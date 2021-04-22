import gzip, io, requests ,csv

from app.common.utils import DictionaryUtil
from app.common.abstracts.AbstractWebhook import AbstractWebhook
from app.domains.AccountDomainService import AccountDomainService
from app.domains.BasketDomainService import BasketDomainService

from app.lib.Smaregi.API.POS.TransactionsApi import TransactionsApi

# from app.domains.TransactionsRepository import TransactionsRepository
# from app.domains.BasketAnalysesRepository import BasketAnalysesRepository

class TransactionsWebhook(AbstractWebhook):
    ACTION_CREATED = 'created'
    EVENT_GET_TRANSACTRION_DETAIL_LIST = 'get_transaction_detail_list'

    def __init__(self, loginAccount):
        super().__init__(loginAccount)
        

    async def received(self, event, body):
        print('transaction webhook received')
        
        if body['action'] == self.ACTION_CREATED:
            _targetTransactionHeadList = body['transactionHeadIds']
            await self.created(_targetTransactionHeadList)
            print(body)


    async def callback(self, event: str, body: dict):
        print(self._accessAccount)
        self._logger.info('transaction callback received')
        
        if event == self.EVENT_GET_TRANSACTRION_DETAIL_LIST:
            urlList = body["file_url"]
            transactionDetailList = []
            for url in urlList:
                response = requests.get(url)
                if response.status_code == 200:
                    gzipFile = io.BytesIO(response.content)
                    with gzip.open(gzipFile, 'rt') as f:
                        data = csv.DictReader(f)
                        for row in data:
                            transactionDetailList.append(row)
            transactionDetailListCategorizedByTransactionHeadId = DictionaryUtil.categorizeByKey('transactionHeadId', transactionDetailList)
            transactionHeadIdFrom = min(transactionDetailListCategorizedByTransactionHeadId.keys())
            transactionHeadIdTo = max(transactionDetailListCategorizedByTransactionHeadId.keys())
            
            self.withSmaregiApi(self._accessAccount.accessToken.accessToken, self._accessAccount.contractId)
            _transactionsApi = TransactionsApi(self._apiConfig)
            whereDict = {
                'transaction_head_id-from': transactionHeadIdFrom,
                'transaction_head_id-to': transactionHeadIdTo,
            }
            transactionHeadList = _transactionsApi.getTransactionHeadList(whereDict=whereDict)
            transactionHeadListCategorizedByTransactionHeadId = DictionaryUtil.categorizeByKey('transactionHeadId', transactionHeadList)
            _basketDomainService = BasketDomainService(self._accessAccount)
            for transactionHeadId in transactionDetailListCategorizedByTransactionHeadId.keys():
                await _basketDomainService.registerBasketByTransaction(
                    transactionHeadListCategorizedByTransactionHeadId[transactionHeadId][0],
                    transactionDetailListCategorizedByTransactionHeadId[transactionHeadId],
                )

    async def created(self, _targetTransactionHeadList):
        _basketDomainService = BasketDomainService(self._accessAccount)
        for _transactionHeadId in _targetTransactionHeadList:
            await _basketDomainService.registerBasketByTransactionHeadId(_transactionHeadId)

    def edited(self):
        pass

    def disposed(self):
        pass

    def canceled(self):
        pass