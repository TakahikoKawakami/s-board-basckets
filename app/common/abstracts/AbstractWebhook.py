from typing import TypeVar, Type
from logging import Logger
from smaregipy import (
    SmaregiPy,
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

        SmaregiPy.init_by_dict({
            'env_division': smaregi_env,
            'contract_id': _contract_id,
            'smaregi_client_id': self._app_config.SMAREGI_CLIENT_ID,
            'smaregi_client_secret': self._app_config.SMAREGI_CLIENT_SECRET,
            'redirect_uri': self._app_config.APP_URI + '/accounts/login',
            'access_token': _access_token,
            'logger': self._logger
        })

        return self
