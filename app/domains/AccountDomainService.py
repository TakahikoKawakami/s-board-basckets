from app.config import AppConfig
from app.common.abstracts.AbstractDomainService import AbstractDomainService
from app.common.globals import globals
from app.common.managers import SessionManager
from app.entities import AccessToken

from app.models import Account, AccountSetting, Store

import datetime

import smaregipy


class AccountDomainService(AbstractDomainService):
    """アカウント関連のドメインサービスクラス

    Args:
        AbstractDomainService ([type]): [description]
    """
    def __init__(self, session):
        self.login_account = None  # [Account]
        super().__init__(self.login_account)
        self._session = session

    def has_contract_id(self) -> bool:
        """sessionに契約IDが入っているか確認します

        Returns:
            bool: true: 有り
        """
        return SessionManager.has(
            self._session,
            SessionManager.KEY_CONTRACT_ID
        )

    async def prepare_for_access_processing(self):
        if self._session is None:
            raise Exception("not set session")
        if not self.has_contract_id():
            raise Exception("not set session")

        _contract_id = SessionManager.get(self._session, SessionManager.KEY_CONTRACT_ID)
        await self.login_by_contract_id(_contract_id)

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
        smaregi_account = smaregipy.account.Account.authenticate(_code, _state)

        _account = await Account.filter(
            contract_id=smaregi_account.contract_id
        ).first()
        if (_account is None):
            SessionManager.set(
                self._session,
                SessionManager.KEY_CONTRACT_ID,
                smaregi_account.contract_id
            )
            await self.login_by_contract_id(smaregi_account.contract_id)
            _account = self.login_account

        return _account

    def get_access_token_by_contract_id(self, contract_id: str) -> 'AccessToken':
        """契約IDからアクセストークンを取得します

        Args:
            contractId (str): [description]

        Returns:
            AccessToken: [description]
        """
        account = smaregipy.account.Account.authorize(
            contract_id,
            [
                'pos.products:read',
                'pos.transactions:read',
                'pos.stores:read',
            ]
        )
        return AccessToken(
            account.access_token.token,
            account.access_token.expiration_datetime
        )

    async def login_by_contract_id(self, _contract_id: str) -> None:
        """契約IDでログインします
        スマレジAPIではなく、look-into-basketsにログインする
        userStatusがstartのもののみ
        また、last-app-versionを保存する

        Args:
            _contractId (str): [description]
        """
        smaregipy.SmaregiPy.init_by_dict({
            'env_division': AppConfig.ENV_DIVISION,
            'contract_id': _contract_id,
            'smaregi_client_id': AppConfig.SMAREGI_CLIENT_ID,
            'smaregi_client_secret': AppConfig.SMAREGI_CLIENT_SECRET,
            'redirect_uri': AppConfig.APP_URI + '/accounts/login'
        })

        _account_model = await Account.filter(
            contract_id=_contract_id,
            user_status=Account.StatusEnum.STATUS_START
            ).first()
        if _account_model is not None:
            _account_model.access_token_entity = (
                self
                .get_access_token_by_contract_id(_contract_id)
            )
            _account_model.last_login_version = AppConfig.APP_VERSION
            await _account_model.save()
            self.login_account = _account_model
            self.login_account.login_status = Account.LoginStatusEnum.SIGN_IN

            globals.login(self.login_account)

            smaregipy.config.update_access_token(
                globals.logged_in_account.access_token_entity
            )

            return

        # それでもなければ取得、dbとセッションに保存
        await self.sign_up_account(_contract_id)

        smaregipy.config.update_access_token(
            globals
            .logged_in_account
            .access_token_entity
        )
        return

    async def sign_up_account(
        self,
        _contract_id: str,
        _plan_name="フリープラン"
    ) -> None:
        """sign upします

        Args:
            _contractId (str): [description]
        """
        _access_token_by_creation = (
            self
            .get_access_token_by_contract_id(_contract_id)
        )
        _plan = Account.PlanEnum.getPlanEnumValue(_plan_name)

        # 存在確認（一度やめて戻ってきた人）
        account = await Account.get_or_none(contract_id=_contract_id)
        if account is not None:
            account.user_status = Account.StatusEnum.STATUS_START
            account.access_token_entity = _access_token_by_creation
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

        self.set_smaregi_api(self.login_account.access_token_entity, self.login_account.contract_id)
        stores_api = StoresApi(self._api_config)
        store_list = stores_api.get_store_list()
        for store in store_list:
            await Store.update_or_create(
                contract_id=self.login_account.contract_id,
                store_id=store.store_id,
                name=store.store_name
            )

        global login_account
        login_account = self.login_account

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

        global login_account
        login_account = self.login_account

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
                access_token.token
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
                await account_setting.serialize()
            )

    async def save_account_setting(self, request):
        account_setting = await AccountSetting.filter(contract_id=self.login_account.contract_id).first()
        account_setting.display_store_id = request['display_store_id']
        account_setting.use_smaregi_webhook = request['use_smaregi_webhook']
        await account_setting.save()
        SessionManager.set(self._session, SessionManager.KEY_TARGET_STORE, account_setting.display_store_id)
        # json = await accountSetting.serialize

        return
