from datetime import datetime

import app.database as db

from app import logger
from app.config import AppConfig
from SmaregiPlatformApi.config import Config as SmaregiConfig


class AbstractDomainService():
    def __init__(self, account):
        self._app_config = None
        self._api_config = None
        self.login_account = account
        self._logger = None

    @classmethod
    async def createInstance(cls, account):
        domain_service = cls(account)
        domain_service._logger = await logger.get_logger(account)
        return domain_service

    def with_smaregi_api(self, _access_token, _contract_id):
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
