from app.common.abstracts.AbstractDomainService import AbstractDomainService
from app.common.managers import SessionManager

import app.database as db
from app.models import Account, AccountSetting, Store

import datetime

from app.lib.Smaregi.API.Authorize import AuthorizeApi
from app.lib.Smaregi.API.POS.StoresApi import StoresApi
from app.lib.Smaregi.entities.Authorize import *

class AccountDomainService(AbstractDomainService):
    """アカウント関連のドメインサービスクラス

    Args:
        AbstractDomainService ([type]): [description]
    """
    def __init__(self, session):
        self.loginAccount = None # [Account]
        super().__init__(self.loginAccount)
        self._session = session
        self.withSmaregiApi(None, None)

    def hasContractId(self) -> bool:
        """sessionに契約IDが入っているか確認します

        Returns:
            bool: true: 有り
        """
        return SessionManager.has(self._session, SessionManager.KEY_CONTRACT_ID)

    async def prepareForAccessProcessing(self):
        if self._session is None:
            raise Exception("not set session")

        # セッション内にあればそれを返す
        _contractId = SessionManager.get(self._session, SessionManager.KEY_CONTRACT_ID)
        # セッションになくDBにあれば（webhookなどの通信）それを返す
        # それでもなければ取得、dbとセッションに保存
        await self.loginByContractId(_contractId)
        self._setAccessTokenDataToSession()
        await self._setAccountSettingToSession()
            
        return

    async def loginByCodeAndState(self, _code, _state):
        """codeとstateでログインします
        スマレジAPIのログイン機能を利用

        Args:
            _code ([type]): [description]
            _state ([type]): [description]

        Raises:
            e: [description]

        Returns:
            [type]: [description]
        """
        _authorizeApi = AuthorizeApi(self._apiConfig, self._appConfig.APP_URI + '/accounts/login')
        try:
            _userInfo = _authorizeApi.getUserInfo(_code, _state)
        except Exception as e:
            raise e
        
        _account = await Account.filter(contract_id = _userInfo.contractId).first()
        if (_account is None):
            SessionManager.set(self._session, SessionManager.KEY_CONTRACT_ID, _userInfo.contractId)
            await self.prepareForAccessProcessing()
            _account = self.loginAccount
            
        return _account

    def getAccessTokenByContractId(self, contractId: str) -> 'AccessToken':
        """契約IDからアクセストークンを取得します

        Args:
            contractId (str): [description]

        Returns:
            AccessToken: [description]
        """
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

    async def loginByContractId(self, _contractId: str) -> None:
        """契約IDでログインします
        スマレジAPIではなく、look-into-basketsにログインする
        userStatusがstartのもののみ

        Args:
            _contractId (str): [description]
        """
        _accountModel = await Account.filter(
            contract_id = _contractId,
            user_status = Account.StatusEnum.STATUS_START
            ).first()
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
        self._setAccessTokenDataToSession()
        return
    
    async def signUpAccount(self, _contractId: str, _planName = "フリープラン") -> None:
        """sign upします

        Args:
            _contractId (str): [description]
        """
        _accessTokenByCreation = self.getAccessTokenByContractId(_contractId)
        _plan = Account.PlanEnum.getPlanEnumValue(_planName)

        # 存在確認（一度やめて戻ってきた人）
        account = await Account.get_or_none(contract_id = _contractId)
        if account is not None:
            account.userStatus = Account.StatusEnum.STATUS_START
            account.accessToken = _accessTokenByCreation
            account.plan = _plan
            await account.save()
            self.loginAccount = account
        else:
            self.loginAccount = await Account.create(
                contractId=_contractId,
                accessToken = _accessTokenByCreation,
                plan = _plan
            )
        self.loginAccount.loginStatus = Account.LoginStatusEnum.SIGN_UP

        self.withSmaregiApi(self.loginAccount.accessToken.accessToken, self.loginAccount.contractId)
        storesApi = StoresApi(self._apiConfig)
        storeList = storesApi.getStoreList()
        for store in storeList:
            newStore = await Store.update_or_create(
                contract_id = self.loginAccount.contractId,
                store_id = store["storeId"],
                name = store["storeName"]
            )

    async def changePlan(self, _contractId: str, _planName) -> None:
        """プランを変更します

        Args:
            _contractId (str): [description]
        """
        self._logger.info("プラン変更開始")
        _accessTokenByCreation = self.getAccessTokenByContractId(_contractId)
        _plan = Account.PlanEnum.getPlanEnumValue(_planName)

        account = await Account.get(contract_id = _contractId)
        if account is not None:
            account.userStatus = Account.StatusEnum.STATUS_START
            account.accessToken = _accessTokenByCreation
            account.plan = _plan
            await account.save()
            self.loginAccount = account
            self._logger.info("アカウント: " + str(self.loginAccount))
        else:
            self._logger.info("アカウントが登録されていません")
            return
        self._logger.info("プラン変更終了")

    async def breakOffAccount(self, contractId: str) -> None:
        """解約します

        Args:
            contractId (str): [description]
        """
        account = await Account.get(contract_id = contractId)
        account.userStatus = Account.StatusEnum.STATUS_STOP
        await account.save()

        self._logger.info("アカウント: " + str(account))

    
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