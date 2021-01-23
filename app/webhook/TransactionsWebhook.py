from app.domains.AccountsDomainService import AccountsDomainService
from app.domains.TransactionsRepository import TransactionsRepository
from app.domains.BasketAnalysesRepository import BasketAnalysesRepository

ACTION_CREATED = 'created'

def received(contractId, event, body):
    _accountsRepository = AccountsRepository().withSmaregiApi(None, contractId)
    _accessToken = _accountsRepository.getAccessTokenByContractId(contractId)['access_token']
    if body['action'] == ACTION_CREATED:
        _targetTransactionHeadList = body['transactionHeadIds']
        _transactionsRepository = TransactionsRepository().withSmaregiApi(_accessToken, contractId)
        _basketAnalysesRepository = BasketAnalysesRepository()
        for _transactionHeadId in _targetTransactionHeadList:
            _transaction = _transactionsRepository.getTransactionById(_transactionHeadId)
            _basketAnalysesRepository.register()
            
            print(body)