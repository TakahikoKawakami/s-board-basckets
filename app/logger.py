import logging
import logging.config
import yaml
import csv

class CsvFormatter(logging.Formatter):
    def format(self, record):
        msg = record.getMessage()
        # convert msg to a csv compatible string using your method of choice
        record.msg = msg
        return super(CsvFormatter, self).format(record) 

class ApplicationLogger(logging.getLoggerClass()):
    def __init__(self, name, level=logging.NOTSET, contract_id=None):
        super().__init__(name, level)
        self._contract_id = None

    @property
    def contract_id(self):
        return self._contract_id

    @contract_id.setter
    def contract_id(self, val):
        self._contract_id = val

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        extra = {
            "contract_id": self.contract_id
        }
        super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)


async def get_logger(account):
    logging.setLoggerClass(ApplicationLogger)
    with open("app/logging_config.yaml", 'r') as f:
        conf_file = yaml.safe_load(f.read())
    logging.config.dictConfig(conf_file)
    logger = logging.getLogger("appLogger")
    logger.contract_id = account.contract_id

    return logger
