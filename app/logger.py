import logging
import logging.config
import yaml
import csv
from typing import cast, Optional


class CsvFormatter(logging.Formatter):
    def format(self, record):
        msg = record.getMessage()
        # convert msg to a csv compatible string using your method of choice
        record.msg = msg
        return super(CsvFormatter, self).format(record)


class ApplicationLogger(logging.getLoggerClass()):
    contract_id: Optional[str]

    def _log(
        self,
        level,
        msg,
        args,
        exc_info=None,
        extra=None,
        stack_info=False,
        stacklevel=1
    ):
        extra = {
            "contract_id": self.contract_id
        }
        super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)


async def get_logger(contract_id: Optional[str]):
    logging.setLoggerClass(ApplicationLogger)
    with open("app/logging_config.yaml", 'r') as f:
        conf_file = yaml.safe_load(f.read())
    logging.config.dictConfig(conf_file)
    logger = cast('ApplicationLogger', logging.getLogger("appLogger"))
    logger.contract_id = contract_id

    return logger
