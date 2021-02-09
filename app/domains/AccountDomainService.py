from app.common.abstracts.AbstractDomainService import AbstractDomainService
from app.common.managers import SessionManager
from app.common.utils import DictionaryUtil

import app.database as db
from app.models import Account, AccountSetting, Store

import json
import datetime
import logging

from app.lib.Smaregi.API.Authorize import AuthorizeApi
from app.lib.Smaregi.API.POS.StoresApi import StoresApi
from app.lib.Smaregi.entities.Authorize import *

class AccountDomainService(AbstractDomainService):
    def __init__(self, session):
        self.loginAccount = None # [Account]
        super().__init__(self.loginAccount)
        self._session = session
        self.withSmaregiApi(None, None)

    def hasContractId(self) -> bool:
        return SessionManager.has(self._session, SessionManager.KEY_CONTRACT_ID)

    async def prepareForAccessProcessing(self):
        if self._session is None:
            raise Exception("not set session")

        # セッション内にあればそれを返す
        _contractId = SessionManager.get(self._session, SessionManager.KEY_CONTRACT_ID)
        # _accessTokenBySession = AccessToken(
        #     SessionManager.get(self._session, SessionManager.KEY_ACCESS_TOKEN),
        #     SessionManager.get(self._session, SessionManager.KEY_ACCESS_TOKEN_EXPIRATION_DATETIME)
        # )
        # _targetStoreId = SessionManager.get(self._session, SessionManager.KEY_TARGET_STORE)
        # if (_accessTokenBySession.isAccessTokenAvailable()):
        #     self.loginAccount = Account()
        #     self.loginAccount.contractId = _contractId
        #     self.loginAccount.accessToken = _accessTokenBySession
            
        #     _accountSettingString = SessionManager.get(self._session, SessionManager.KEY_ACCOUNT_SETTING)
        #     _accountSettingJson = json.loads(_accountSettingString)

        #     setting = AccountSetting()
        #     setting.id = _accountSettingJson['id']
        #     setting.contractId = _accountSettingJson['contract_id']
        #     setting.createdAt = _accountSettingJson['created_at']
        #     setting.modifiedAt = _accountSettingJson['modified_at']
        #     setting.displayStoreId = _accountSettingJson['display_store_id']
        #     setting.useSmaregiWebhook = _accountSettingJson['use_smaregi_webhook']
        #     self.loginAccount.account_setting = setting
            
        #     self.loginAccount.loginStatus = Account.LoginStatusEnum.SIGN_ON
        #     return
        # セッションになくDBにあれば（webhookなどの通信）それを返す
        # それでもなければ取得、dbとセッションに保存
        await self.loginByContractId(_contractId)
        self._setAccessTokenDataToSession()
        await self._setAccountSettingToSession()
            
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
            self.loginAccount = _accountModel
            self.loginAccount.loginStatus = Account.LoginStatusEnum.SIGN_IN
            return
        
        # それでもなければ取得、dbとセッションに保存
        await self.signUpAccount(_contractId)
        return
    
    async def signUpAccount(self, _contractId):
        _accessTokenByCreation = self.getAccessTokenByContractId(_contractId)
        self.loginAccount = await Account.create(
            contractId=_contractId,
            accessToken = _accessTokenByCreation
        )
        self.loginAccount.loginStatus = Account.LoginStatusEnum.SIGN_UP

        self.withSmaregiApi(self.loginAccount.accessToken.accessToken, self.loginAccount.contractId)
        storesApi = StoresApi(self._apiConfig)
        storeList = storesApi.getStoreList()
        for store in storeList:
            newStore = await Store.create(
                contract_id = self.loginAccount.contractId,
                store_id = store["storeId"],
                name = store["storeName"]
            )
        
        self._setAccessTokenDataToSession()
    
    def _setAccessTokenDataToSession(self):
        accessToken = self.loginAccount.accessToken
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

    async def _setAccountSettingToSession(self):
        accountSetting = await self.loginAccount.accountSetting
        if self._session is not None:
            SessionManager.set(
                self._session,
                SessionManager.KEY_ACCOUNT_SETTING,
                await accountSetting.serialize
            )

    async def saveAccountSetting(self, request):
        accountSetting = await AccountSetting.filter(contract_id = self.loginAccount.contractId).first()
        accountSetting.displayStoreId = request['display_store_id']
        accountSetting.use_smaregi_webhook = request['use_smaregi_webhook']
        await accountSetting.save()
        SessionManager.set(self._session, SessionManager.KEY_TARGET_STORE, accountSetting.displayStoreId)
        # json = await accountSetting.serialize
        return