from app.common.abstracts.AbstractDomainService import AbstractDomainService
from app.common.managers import SessionManager
from app.common.utils import DictionaryUtil

import app.database as db
from app.models.Accounts import Account

import datetime
import logging

from app.lib.Smaregi.API.Authorize import AuthorizeApi
from app.lib.Smaregi.entities.Authorize import *

class AccountsDomainService(AbstractDomainService):
    def __init__(self, session):
        super().__init__(session)

        self._logger = logging.getLogger(__name__)
        self.withSmaregiApi(None, None)


    def hasContractId(self) -> bool:
        return SessionManager.has(self._session, SessionManager.KEY_CONTRACT_ID)

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


    async def getContractIdAndAccessToken(self):
        # セッション内にあればそれを返す
        _contractId = SessionManager.get(self._session, SessionManager.KEY_CONTRACT_ID)

        if self._session is not None:
            _accessTokenBySession = AccessToken(
                SessionManager.get(self._session, SessionManager.KEY_ACCESS_TOKEN),
                SessionManager.get(self._session, SessionManager.KEY_ACCESS_TOKEN_EXPIRES_IN)
            )
            if (AccountsDomainService._isAccessTokenAvailable(_accessTokenBySession)):
                return _contractId, _accessTokenBySession

        # セッションになくDBにあれば（webhookなどの通信）それを返す
        _accountModel = await Account.filter(contract_id=_contractId).first()
        if (_accountModel is not None):
            _accessTokenByDatabase = AccessToken(
                accountModel.accessToken,
                accountModel.expirationDateTime
            )
            return _contractId, _accessTokenByDatabase

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
        _newAccountModel = await Account.create(
            contractId=_contractId,
            accessToken = _result
        )

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


    async def loginByCodeAndState(self, _code, _state):
        _authorizeApi = AuthorizeApi(self._apiConfig, self._appConfig.APP_URI + '/accounts/login')
        _userInfo = _authorizeApi.getUserInfo(_code, _state)
        
        _account = await Account.filter(contract_id = _userInfo.contractId).first()
        if (_account is None):
            _newAccount = Account()
            _newAccount.contractId = _userInfo.contractId
            _newAccount.status = Account.STATUS_START
            _newAccount.accessToken = None
            _newAccount.expirationDateTime = None
            _newAccount.save()
            _account = _newAccount
            
        return _account
