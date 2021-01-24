import datetime
import pytz

class UserInfo():
    def __init__(self, json):
        self._sub = json['sub']
        self._contractId = json['contract']['id']
        self._isOwner = json['contract']['is_owner']

    
    @property
    def contractId(self):
        return self._contractId


class UserAccessToken():
    def __init__(self, _accessToken):
        self._accessToken = _accessToken
    

    @property
    def accessToken(self):
        return self._accessToken


class AccessToken():
    def __init__(self, _accessToken, _expirationDatetime):
        self.accessToken = _accessToken
        self.expirationDatetime = _expirationDatetime

    @property
    def accessToken(self):
        return self._accessToken

    @accessToken.setter
    def accessToken(self, value):
        self._accessToken = value

    @property
    def expirationDatetime(self):
        return self._expirationDatetime

    @expirationDatetime.setter
    def expirationDatetime(self, value):
        if type(value) == str:
            value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S %z')
        self._expirationDatetime = value
        
    def isAccessTokenAvailable(self):
        if self.accessToken is None:
            return False
        if self.expirationDatetime is not None:
            now = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
            if (self.expirationDatetime < now):
                return False
        return True
