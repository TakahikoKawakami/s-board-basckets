from typing import TypeVar, Type
from logging import Logger
from smaregipy import (
    SmaregiPy,
    smaregi_config,
    Config as SmaregiConfig
)

from app import logger
from app.models.Accounts import Account
from app.common.globals import globals
from app.config import AppConfig
from app.entities.AccessToken import AccessToken

T = TypeVar('T', bound='AbstractDomainService')


class AbstractDomainService():
    _app_config: AppConfig
    login_account: Account
    _logger: Logger

    def __init__(self, account: Account):
        self._app_config = AppConfig()
        self.login_account = globals.logged_in_account

    @classmethod
    async def create_instance(cls: Type[T], account: Account) -> T:
        domain_service = cls(account)
        domain_service._logger = \
            await logger.get_logger(account.contract_id)
        # domain_service.set_smaregi_api(
        #     domain_service.login_account.access_token_entity,
        #     domain_service.login_account.contract_id
        # )
        return domain_service

    # def with_smaregi_api(
    #     self,
    #     _access_token: AccessToken,
    #     _contract_id
    # ):
    #     if self._app_config.ENV_DIVISION in (
    #         AppConfig.ENV_DIVISION_MOCK,
    #         AppConfig.ENV_DIVISION_LOCAL,
    #         AppConfig.ENV_DIVISION_STAGING,
    #     ):
    #         smaregi_env = SmaregiConfig.ENV_DIVISION_DEVELOPMENT
    #     else:
    #         smaregi_env = SmaregiConfig.ENV_DIVISION_PRODUCTION

    #     config = SmaregiConfig(
    #         smaregi_env,
    #         _contract_id,
    #         self._app_config.SMAREGI_CLIENT_ID,
    #         self._app_config.SMAREGI_CLIENT_SECRET,
    #         _access_token,
    #         self._logger
    #     )
    #     SmaregiPy.init_by_dict({
    #         'env_division': smaregi_env,
    #         'contract_id': dictionary.get('contract_id'),
    #         'redirect_uri': dictionary.get('redirect_uri'),
    #         'smaregi_client_id': dictionary.get('smaregi_client_id'),
    #         'smaregi_client_secret': dictionary.get('smaregi_client_secret'),
    #         'access_token': dictionary.get('access_token'),
    #         'logger': dictionary.get('logger'),
    #     })

    #     return self

    def set_smaregi_api(
        self,
        _access_token: AccessToken,
        _contract_id
    ):
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
