from typing import TypeVar, Type, Optional
from logging import Logger
from app import logger
from app.models.Accounts import Account
from app.config import AppConfig
from SmaregiPlatformApi.config import Config as SmaregiConfig
from app.entities.AccessToken import AccessToken

T = TypeVar('T', bound='AbstractDomainService')


class AbstractDomainService():
    def __init__(self, account):
        self._app_config: Optional[AppConfig] = None
        self._api_config: Optional[SmaregiConfig] = None
        self.login_account: Optional[Account] = account
        self._logger: Optional[Logger] = None

    @classmethod
    async def create_instance(cls: Type[T], account: Optional['Account']) -> T:
        domain_service = cls(account)
        if isinstance(account, Account):
            domain_service._logger = \
                await logger.get_logger(account.contract_id)
        return domain_service

    def with_smaregi_api(
        self,
        _access_token: Optional[AccessToken],
        _contract_id
    ):
        self._app_config = AppConfig()
        self._api_config = SmaregiConfig(
            self._app_config.ENV_DIVISION,
            self._app_config.SMAREGI_CLIENT_ID,
            self._app_config.SMAREGI_CLIENT_SECRET
        )
        if _access_token is not None:
            self._api_config.access_token = _access_token
        self._api_config.contract_id = _contract_id

        return self
