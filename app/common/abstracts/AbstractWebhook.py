from typing import TypeVar, Type
from logging import Logger
from SmaregiPlatformApi import (
    smaregi_config,
    Config as SmaregiConfig
)
from app import logger
from app.models import Account
from app.config import AppConfig
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
            webhook._logger = await logger.get_logger(account.contract_id)
        return webhook

    def with_smaregi_api(
        self,
        _access_token: AccessToken,
        _contract_id
    ):
        self._app_config = AppConfig()
        if self._app_config.ENV_DIVISION in (
            AppConfig.ENV_DIVISION_MOCK,
            AppConfig.ENV_DIVISION_LOCAL,
            AppConfig.ENV_DIVISION_STAGING,
        ):
            smaregi_env = SmaregiConfig.ENV_DIVISION_DEVELOPMENT
        else:
            smaregi_env = SmaregiConfig.ENV_DIVISION_PRODUCTION

        config = SmaregiConfig(
            smaregi_env,
            _contract_id,
            self._app_config.SMAREGI_CLIENT_ID,
            self._app_config.SMAREGI_CLIENT_SECRET,
            _access_token,
            self._logger
        )
        smaregi_config.set_by_object(config)

        return self
