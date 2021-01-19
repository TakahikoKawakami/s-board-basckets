import base64

from .BaseApi import BaseApi

class BaseIdentificationApi(BaseApi):
    def _showAuthorizationString(self):
        return (
            self.config.smaregiClientId + 
            ":" + 
            self.config.smaregiClientSecret
        ).encode()
           
         
    def _getSmaregiAuth(self):
        string = self._showAuthorizationString()
        base = self._getBase64Encode(string)
        return "Basic " + str(base).split("'")[1]
        
    
    def _getHeader(self):
        return {
            'Authorization': self._getSmaregiAuth(),
            'Content-Type':	'application/x-www-form-urlencoded',        
        }

