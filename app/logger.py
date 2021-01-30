import logging
import logging.config
import yaml

class ApplicationLogger():
    def __init__(self, account):
        with open("app/logging_config.yaml", 'r') as f:
            conf_file = yaml.safe_load(f.read())
        logging.config.dictConfig(conf_file)
        self._logger = logging.getLogger("appLogger")
        self._account = account

    def debug(self, val):
        self._logger.debug(val, extra={"contractId": self._account.contractId})

    def info(self, val):
        self._logger.info(val, extra={"contractId": self._account.contractId})

    def warn(self, val):
        self._logger.warn(val, extra={"contractId": self._account.contractId})

    def error(self, val):
        self._logger.error(val, extra={"contractId": self._account.contractId})