from .BaseApi import BaseApi

class BaseIdentificationApi(BaseApi):
    def _show_authorization_string(self):
        return (
            self.config.smaregiClientId +
            ":" +
            self.config.smaregiClientSecret
        ).encode()

    def _get_smaregi_auth(self):
        string = self._show_authorization_string()
        base = self._get_base64_encode(string)
        return "Basic " + str(base).split("'")[1]

    def _get_header(self):
        return {
            'Authorization': self._get_smaregi_auth(),
            'Content-Type':	'application/x-www-form-urlencoded',
        }
