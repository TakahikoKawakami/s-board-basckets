import base64

class BaseApi():
    def __init__(self, config):
        self.config = config
        
    
    def _getBase64Encode(self):
        return base64.b64encode(
            (
                self.config.smaregiClientId + 
                ":" + 
                self.config.smaregiClientSecret).encode()
        )
        
        
    def _getSmaregiAuth(self):
        base = self._getBase64Encode()
        return "Basic " + str(base).split("'")[1]
        
    
    def _getHeader(self):
        return {
            'Authorization': self._getSmaregiAuth(),
            'Content-Type':	'application/x-www-form-urlencoded',        
        }
