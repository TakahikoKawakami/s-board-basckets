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
    def __init__(self, name, level=logging.NOTSET, contractId=None):
        super().__init__(name, level)
        self._contractId = None

    @property
    def contractId(self):
        return self._contractId

    @contractId.setter
    def contractId(self, val):
        self._contractId = val

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        extra = {
            "contractId": self.contractId
        }
        super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)


async def getLogger(account):
    # import pdb; pdb.set_trace()
    logging.setLoggerClass(ApplicationLogger)
    with open("app/logging_config.yaml", 'r') as f:
        conf_file = yaml.safe_load(f.read())
    logging.config.dictConfig(conf_file)
    logger = logging.getLogger("appLogger")
    logger.contractId = account.contractId

    return logger
