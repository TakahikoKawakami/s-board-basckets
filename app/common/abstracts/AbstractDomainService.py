from datetime import datetime

import app.database as db

from app import logger
from app.config import AppConfig
from app.lib.Smaregi.config import config as SmaregiConfig

class AbstractDomainService():
    def __init__(self, account):
        self._appConfig = None
        self._apiConfig = None
        self._loginAccount = account
        self._logger = None
    
    @classmethod
    async def createInstance(cls, account):
        domainService = cls(account)
        domainService._logger = await logger.getLogger(account)
        return domainService


    def withSmaregiApi(self, _accessToken, _contractId):
        self._appConfig = AppConfig()
        self._apiConfig = SmaregiConfig(
            self._appConfig.ENV_DIVISION,
            self._appConfig.SMAREGI_CLIENT_ID,
            self._appConfig.SMAREGI_CLIENT_SECRET,
            self._logger
        )
        self._apiConfig.accessToken = _accessToken
        self._apiConfig.contractId = _contractId

        return self


    def with_smaregi_api_for_support_login(self, contract_id, client_id, secret_id, access_token):
        self._appConfig = AppConfig()
        self._apiConfig = SmaregiConfig(
            "PROD",
            client_id,
            secret_id,
            self._logger
        )
        self._apiConfig.accessToken = access_token
        self._apiConfig.contractId = contract_id

        return self

