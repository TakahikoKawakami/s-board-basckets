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
        return
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        sinfo = None
        if _srcfile:
            #IronPython doesn't track Python frames, so findCaller raises an
            #exception on some versions of IronPython. We trap it here so that
            #IronPython can use logging.
            try:
                fn, lno, func, sinfo = self.findCaller(stack_info, stacklevel)
            except ValueError: # pragma: no cover
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else: # pragma: no cover
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.makeRecord(self.name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
        self.handle(record)

async def getLogger(account):
    logging.setLoggerClass(ApplicationLogger)
    with open("app/logging_config.yaml", 'r') as f:
        conf_file = yaml.safe_load(f.read())
    logging.config.dictConfig(conf_file)
    logger = logging.getLogger("appLogger")
    logger.contractId = account.contractId

    return logger
