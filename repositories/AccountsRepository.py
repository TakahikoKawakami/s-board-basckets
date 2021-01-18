from common.abstracts.AbstractRepository import AbstractRepository
from common.managers import SessionManager
from common.utils import DictionaryUtil

import database as db
from models.Accounts import Account

import datetime
import logging

from lib.Smaregi.API.Authorize import AuthorizeApi
from lib.Smaregi.entities.Authorize import *

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

    @staticmethod
    def getByContractId(contractId):
        result = db.session.query(Account)\
            .filter(Account.contractId == contractId).first()
        return result


    def getAccessTokenByContractId(self, _contractId):
        # セッション内にあればそれを返す
        accessTokenBySession = AccessToken(
            SessionManager.get(SessionManager.KEY_ACCESS_TOKEN),
            SessionManager.get(SessionManager.KEY_ACCESS_TOKEN_EXPIRES_IN)
        )
        if (AccountsRepository._isAccessTokenAvailable(accessTokenBySession)):
            return accessTokenBySession

        # セッションになくDBにあれば（webhookなどの通信）それを返す
        accountModel = AccountsRepository.getByContractId(_contractId)
        if (accountModel is not None):
            accessTokenByDatabase = AccessToken(
                accountModel.accessToken,
                accountModel.expirationDateTime
            )
            return accessTokenByDatabase

        # それでもなければ取得、dbとセッションに保存
        _authorizeApi = AuthorizeApi(self._apiConfig, self._appConfig.APP_URI + '/accounts/login')
        _result = _authorizeApi.getAccessToken(
            _contractId,
            [
                'pos.products:read',
                'pos.transactions:read',
                'pos.stores:read',
            ]
        )
        accountModel.accessToken = _result.accessToken
        accountModel.expirationDatetime = _result.expirationDatetime
        AccountsRepository.registerAccount(accountModel)
        SessionManager.set(SessionManager.KEY_ACCESS_TOKEN, _result.accessToken)
        SessionManager.set(SessionManager.KEY_ACCESS_TOKEN_EXPIRES_IN, _result.expirationDatetime)

        return _result

        # どちらもなければ、更新する
        

    def _isAccessTokenAvailable(accessTokenEntity):
        if accessTokenEntity.accessToken is None:
            return False
        if accessTokenEntity.expirationDatetime is not None:
            now = datetime.datetime.now()
            if (accessTokenEntity.expirationDatetime < now):
                return False
        return True