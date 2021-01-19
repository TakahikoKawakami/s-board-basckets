from app.common.abstracts.AbstractRepository import AbstractRepository
from app.common.managers import SessionManager
from app.common.utils import DictionaryUtil

import app.database as db
from app.models.Accounts import Account

import datetime
import logging

from app.lib.Smaregi.API.Authorize import AuthorizeApi
from app.lib.Smaregi.entities.Authorize import *

class AccountsRepository(AbstractRepository):
    def __init__(self, session):
        super().__init__(session)

        self._logger = logging.getLogger('flask.app')


    def registerAccount(self, model):
        if model.contractId is None:
            model.contractId = SessionManager.get(self._session, SessionManager.KEY_CONTRACT_ID)
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
            .filter(Account.contract_id == contractId).first()
        return result


    def getAccessTokenByContractId(self, _contractId, session = None):
        # セッション内にあればそれを返す
        if session is not None:
            accessTokenBySession = AccessToken(
                SessionManager.get(session, SessionManager.KEY_ACCESS_TOKEN),
                SessionManager.get(session, SessionManager.KEY_ACCESS_TOKEN_EXPIRES_IN)
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
        self.registerAccount(accountModel)
        SessionManager.set(session, SessionManager.KEY_ACCESS_TOKEN, _result.accessToken)
        SessionManager.set(session, SessionManager.KEY_ACCESS_TOKEN_EXPIRES_IN, _result.expirationDatetime)

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


    def loginByCodeAndState(self, _code, _state):
        _authorizeApi = AuthorizeApi(self._apiConfig, self._appConfig.APP_URI + '/accounts/login')
        _userInfo = _authorizeApi.getUserInfo(_code, _state)
        
        account = AccountsRepository.getByContractId(_userInfo.contractId)
        if (account is None):
            newAccount = Account()
            newAccount.contractId = _userInfo.contractId
            newAccount.status = Account.STATUS_START
            newAccount.accessToken = None
            newAccount.expirationDateTime = None
            account = self.registerAccount(newAccount)
            AccountsRepository.commit()
            
        return account
