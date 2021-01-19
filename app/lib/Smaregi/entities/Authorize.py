import datetime

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
    def __init__(self, _accessToken, _expiresIn):
        self._accessToken = _accessToken
        self._expiresIn = _expiresIn

    @property
    def accessToken(self):
        return self._accessToken


    @property
    def expirationDateTime(self):
        return datetime.datetime.now() + datetime.timedelta(seconds=self._expiresIn)

