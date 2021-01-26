from app.common.abstracts.AbstractDomainService import AbstractDomainService
from app.common.managers import SessionManager
from app.common.utils import DictionaryUtil

import app.database as db
from app.models import Account

import datetime
import logging

from app.lib.Smaregi.API.Authorize import AuthorizeApi
from app.lib.Smaregi.entities.Authorize import *

class AccountsDomainService(AbstractDomainService):
    def __init__(self, session):
        super().__init__(session)

        self._logger = logging.getLogger(__name__)
        self.withSmaregiApi(None, None)

        self.loginAccount = None # [Account]

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

    async def prepareForAccessProcessing(self):
        if self._session is None:
            raise Exception("not set session")

        # セッション内にあればそれを返す
        _contractId = SessionManager.get(self._session, SessionManager.KEY_CONTRACT_ID)
        _accessTokenBySession = AccessToken(
            SessionManager.get(self._session, SessionManager.KEY_ACCESS_TOKEN),
            SessionManager.get(self._session, SessionManager.KEY_ACCESS_TOKEN_EXPIRATION_DATETIME)
        )
        if (_accessTokenBySession.isAccessTokenAvailable()):
            self.loginAccount = Account()
            self.loginAccount.contractId = _contractId
            self.loginAccount.accessToken = _accessTokenBySession
            return
        # セッションになくDBにあれば（webhookなどの通信）それを返す
        # それでもなければ取得、dbとセッションに保存
        await self.loginByContractId(_contractId)
        return

    async def loginByCodeAndState(self, _code, _state):
        _authorizeApi = AuthorizeApi(self._apiConfig, self._appConfig.APP_URI + '/accounts/login')
        _userInfo = _authorizeApi.getUserInfo(_code, _state)
        
        _account = await Account.filter(contract_id = _userInfo.contractId).first()
        if (_account is None):
            SessionManager.set(self._session, SessionManager.KEY_CONTRACT_ID, _userInfo.contractId)
            await self.prepareForAccessProcessing()
            _account = self.loginAccount
            
        return _account

    def getAccessTokenByContractId(self, contractId):
        _authorizeApi = AuthorizeApi(self._apiConfig, self._appConfig.APP_URI + '/accounts/login')
        _accessTokenByCreation = _authorizeApi.getAccessToken(
            contractId,
            [
                'pos.products:read',
                'pos.transactions:read',
                'pos.stores:read',
            ]
        )
        return _accessTokenByCreation

    async def loginByContractId(self, _contractId):
        # セッションになくDBにあれば（webhookなどの通信）それを返す
        _accountModel = await Account.filter(contract_id=_contractId).first()
        if _accountModel is not None: 
            if not _accountModel.accessToken.isAccessTokenAvailable():
                _accessTokenForUpdate = self.getAccessTokenByContractId(_contractId)
                _accountModel.accessToken = _accessTokenForUpdate
                await _accountModel.save()
            else:
                _accessTokenForUpdate = _accountModel.accessToken
            self._setAccessTokenDataToSession(_accessTokenForUpdate)
            self.loginAccount = _accountModel
            return

        # それでもなければ取得、dbとセッションに保存
        _accessTokenByCreation = self.getAccessTokenByContractId(_contractId)
        self.loginAccount = await Account.create(
            contractId=_contractId,
            accessToken = _accessTokenByCreation
        )
        self._setAccessTokenDataToSession(_accessTokenByCreation)
        return
    
    def _setAccessTokenDataToSession(self, accessToken):
        if self._session is not None:
            SessionManager.set(
                self._session, 
                SessionManager.KEY_ACCESS_TOKEN, 
                accessToken.accessToken
            )
            SessionManager.set(
                self._session, 
                SessionManager.KEY_ACCESS_TOKEN_EXPIRATION_DATETIME, 
                datetime.datetime.strftime(accessToken.expirationDatetime, '%Y-%m-%d %H:%M:%S %z')
            )