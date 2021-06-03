from app.common.abstracts.AbstractDomainService import AbstractDomainService
from app.common.managers import SessionManager

from app.models import Account, AccountSetting, Store

import datetime

from SmaregiPlatformApi.authorize import AuthorizeApi
from SmaregiPlatformApi.entities.authorize import AccessToken
from SmaregiPlatformApi.pos import StoresApi


class AccountDomainService(AbstractDomainService):
    """アカウント関連のドメインサービスクラス

    Args:
        AbstractDomainService ([type]): [description]
    """
    def __init__(self, session):
        self.login_account = None  # [Account]
        super().__init__(self.login_account)
        self._session = session
        self.with_smaregi_api(None, None)

    def has_contract_id(self) -> bool:
        """sessionに契約IDが入っているか確認します

        Returns:
            bool: true: 有り
        """
        return SessionManager.has(self._session, SessionManager.KEY_CONTRACT_ID)

    async def prepare_for_access_processing(self):
        if self._session is None:
            raise Exception("not set session")
        if not self.has_contract_id():
            raise Exception("not set session")

        # セッション内にあればそれを返す
        _contract_id = SessionManager.get(self._session, SessionManager.KEY_CONTRACT_ID)
        # セッションになくDBにあれば（webhookなどの通信）それを返す
        # それでもなければ取得、dbとセッションに保存
        await self.login_by_contract_id(_contract_id)
        # self._set_access_token_data_to_session()
        # await self._set_account_setting_to_session()
            
        return

    async def login_by_code_and_state(self, _code, _state) -> 'Account':
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
        _authorize_api = AuthorizeApi(
            self._api_config,
            self._app_config.APP_URI + '/accounts/login'
        )
        try:
            _user_info = _authorize_api.get_user_info(_code, _state)
        except Exception as e:
            raise e

        _account = await Account.filter(
            contract_id=_user_info.contract_id
        ).first()
        if (_account is None):
            SessionManager.set(
                self._session,
                SessionManager.KEY_CONTRACT_ID,
                _user_info.contract_id
            )
            await self.prepare_for_access_processing()
            _account = self.login_account

        return _account

    def get_access_token_by_contract_id(self, contract_id: str) -> 'AccessToken':
        """契約IDからアクセストークンを取得します

        Args:
            contractId (str): [description]

        Returns:
            AccessToken: [description]
        """
        _authorize_api = AuthorizeApi(self._api_config, self._app_config.APP_URI + '/accounts/login')
        _access_token_by_creation = _authorize_api.get_access_token(
            contract_id,
            [
                'pos.products:read',
                'pos.transactions:read',
                'pos.stores:read',
            ]
        )
        return _access_token_by_creation

    async def login_by_contract_id(self, _contract_id: str) -> None:
        """契約IDでログインします
        スマレジAPIではなく、look-into-basketsにログインする
        userStatusがstartのもののみ

        Args:
            _contractId (str): [description]
        """
        _account_model = await Account.filter(
            contract_id=_contract_id,
            user_status=Account.StatusEnum.STATUS_START
            ).first()
        if _account_model is not None:
            if not _account_model.access_token_entity.is_access_token_available():
                _accessTokenForUpdate = self.get_access_token_by_contract_id(_contract_id)
                _account_model.access_token = _accessTokenForUpdate
                await _account_model.save()
            else:
                _accessTokenForUpdate = _account_model.access_token
            self.login_account = _account_model
            self.login_account.login_status = Account.LoginStatusEnum.SIGN_IN
            return

        # それでもなければ取得、dbとセッションに保存
        await self.signUpAccount(_contract_id)
        # self._set_access_token_data_to_session()
        return


    async def signUpAccount(self, _contract_id: str, _plan_name="フリープラン") -> None:
        """sign upします

        Args:
            _contractId (str): [description]
        """
        _access_token_by_creation = self.get_access_token_by_contract_id(_contract_id)
        _plan = Account.PlanEnum.getPlanEnumValue(_plan_name)

        # 存在確認（一度やめて戻ってきた人）
        account = await Account.get_or_none(contract_id=_contract_id)
        if account is not None:
            account.user_status = Account.StatusEnum.STATUS_START
            account.access_token = _access_token_by_creation
            account.plan = _plan
            await account.save()
            self.login_account = account
        else:
            self.login_account = await Account.create(
                contract_id=_contract_id,
                access_token=_access_token_by_creation,
                plan=_plan
            )
        self.login_account.login_status = Account.LoginStatusEnum.SIGN_UP

        self.with_smaregi_api(self.login_account.access_token_entity.access_token, self.login_account.contract_id)
        stores_api = StoresApi(self._api_config)
        store_list = stores_api.get_store_list()
        for store in store_list:
            await Store.update_or_create(
                contract_id=self.login_account.contract_id,
                store_id=store.store_id,
                name=store.store_name
            )

    async def changePlan(self, _contractId: str, _planName) -> None:
        """プランを変更します

        Args:
            _contractId (str): [description]
        """
        self._logger.info("プラン変更開始")
        _accessTokenByCreation = self.getAccessTokenByContractId(_contractId)
        _plan = Account.PlanEnum.getPlanEnumValue(_planName)

        account = await Account.get(contract_id=_contractId)
        if account is not None:
            account.userStatus = Account.StatusEnum.STATUS_START
            account.accessToken = _accessTokenByCreation
            account.plan = _plan
            await account.save()
            self.login_account = account
            self._logger.info("アカウント: " + str(self.login_account))
        else:
            self._logger.info("アカウントが登録されていません")
            return
        self._logger.info("プラン変更終了")

    async def breakOffAccount(self, contractId: str) -> None:
        """解約します

        Args:
            contractId (str): [description]
        """
        account = await Account.get(contract_id=contractId)
        account.user_status = Account.StatusEnum.STATUS_STOP
        await account.save()

        self._logger.info("アカウント: " + str(account))

    def _set_access_token_data_to_session(self):
        access_token = self.login_account.access_token_entity
        if self._session is not None:
            SessionManager.set(
                self._session,
                SessionManager.KEY_ACCESS_TOKEN,
                access_token.access_token
            )
            SessionManager.set(
                self._session,
                SessionManager.KEY_ACCESS_TOKEN_EXPIRATION_DATETIME,
                datetime.datetime.strftime(access_token.expiration_datetime, '%Y-%m-%d %H:%M:%S %z')
            )

    async def _set_account_setting_to_session(self):
        account_setting = await self.login_account.account_setting_model
        if self._session is not None:
            SessionManager.set(
                self._session,
                SessionManager.KEY_ACCOUNT_SETTING,
                account_setting.serialize
            )

    async def saveAccountSetting(self, request):
        account_setting = await AccountSetting.filter(contract_id=self.login_account.contract_id).first()
        account_setting.display_store_id = request['display_store_id']
        account_setting.use_smaregi_webhook = request['use_smaregi_webhook']
        await account_setting.save()
        SessionManager.set(self._session, SessionManager.KEY_TARGET_STORE, account_setting.display_store_id)
        # json = await accountSetting.serialize
        return
