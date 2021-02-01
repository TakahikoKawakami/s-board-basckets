from app.domains.AccountDomainService import AccountDomainService
from app.domains.BasketDomainService import BasketDomainService
# from app.domains.TransactionsRepository import TransactionsRepository
# from app.domains.BasketAnalysesRepository import BasketAnalysesRepository

class TransactionsWebhook():
    ACTION_CREATED = 'created'

    def __init__(self):
        self._accessAccount = None
        print('transaction webhook init')

    async def received(self, contractId, event, body):
        print('transaction webhook received')
        _accountDomainService = AccountDomainService(None)
        await _accountDomainService.loginByContractId(contractId)
        self._accessAccount = _accountDomainService.loginAccount
        print(self._accessAccount)
        if body['action'] == self.ACTION_CREATED:
            _targetTransactionHeadList = body['transactionHeadIds']
            await self.created(_targetTransactionHeadList)
            print(body)

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