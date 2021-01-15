import common.managers.SessionManager as sessionManager
from common.abstracts.AbstractRepository import AbstractRepository
import datetime
from authorizations.models.Accounts import Account
from common.utils import DictionaryUtil
import logging

from lib.Smaregi.API.Authorize import AuthorizeApi

class AccountsRepository(AbstractRepository):
    def __init__(self):
        super().__init__()

        self._logger = logging.getLogger('flask.app')


    @staticmethod
    def registerAccount(model):
        model.contractId = sessionManager.getByKey(sessionManager.KEY_CONTRACT_ID)
        model.createdAt = datetime.datetime.now()
        model.modifiedAt = datetime.datetime.now()
        return model.register()


    @staticmethod
    def getActiveAccountList():
        result = db.session.query(Account)\
            .filter(Account.status == Account.STATUS_START).all()
        return result


    def getAccessTokenByContractId(self, _contractId):
        _authorizeApi = AuthorizeApi(self._apiConfig, self._appConfig.APP_URI + '/accounts/login')
        _resultList = _authorizeApi.getAccessToken(
            _contractId,
            [
                'pos.products:read',
                'pos.transactions:read',
                'pos.stores:read',
            ]
        )