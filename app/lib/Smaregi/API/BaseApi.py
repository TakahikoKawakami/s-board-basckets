import base64
from ..config import config

class BaseApi():
    def __init__(self, config: 'config'):
        self.config = config
        # self.logger = self.config.logger


    def _getBase64Encode(self, string):
        return base64.b64encode(string)

    

