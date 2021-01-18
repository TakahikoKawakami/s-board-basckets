from datetime import datetime

import database as db

from config import AppConfig
from lib.Smaregi.config import config as SmaregiConfig

class AbstractRepository():
    def __init__(self):
        self._appConfig = None
        self._apiConfig = None


    @staticmethod
    def commit():
        db.session.commit()
        

    @staticmethod
    def rollback():
        db.session.rollback()
    

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

