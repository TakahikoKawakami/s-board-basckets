from app.lib.Smaregi.entities import Authorize

class AccessToken(Authorize.AccessToken):
    def __init__(self, _accessToken, _expirationDatetime):
        super().__init__(_accessToken, _expirationDatetime)
