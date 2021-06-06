from typing import TypeVar, Type
from logging import Logger
from app import logger
from app.models import Account
from app.config import AppConfig
from SmaregiPlatformApi import Config as SmaregiConfig
from app.entities.AccessToken import AccessToken


T = TypeVar('T', bound="AbstractWebhook")


class AbstractWebhook():
    def __init__(self, account: 'Account'):
        self._access_account: 'Account' = account
        self._logger: Logger

    @classmethod
    async def create_instance(cls: Type[T], account: 'Account') -> T:
        webhook = cls(account)
        if account is not None:
            webhook._logger = await logger.get_logger(account)
        return webhook

    def with_smaregi_api(
        self,
        _access_token: "AccessToken",
        _contract_id: str
    ):
        self._app_config = AppConfig()
        self._api_config = SmaregiConfig(
            self._app_config.ENV_DIVISION,
            self._app_config.SMAREGI_CLIENT_ID,
            self._app_config.SMAREGI_CLIENT_SECRET,
            self._logger
        )
        self._api_config.access_token = _access_token
        self._api_config.contract_id = _contract_id

        return self
