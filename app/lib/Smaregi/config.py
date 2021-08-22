import datetime

class config():
    ENV_DIVISION_MOCK = 'MOCK'
    ENV_DIVISION_LOCAL = 'LOCAL'
    ENV_DIVISION_STAGING = 'STAGING'
    ENV_DIVISION_PRODUCTION = 'PROD'
    
    def __init__(self, env_division, clientId, clientSecret, logger=None):
        if (env_division in (self.ENV_DIVISION_MOCK, self.ENV_DIVISION_LOCAL, self.ENV_DIVISION_STAGING)):
            self.uriAccess = 'https://id.smaregi.dev'
            self.uriApi = 'https://api.smaregi.dev'
        else:
            self.uriAccess = 'https://id.smaregi.jp'
            self.uriApi = 'https://api.smaregi.jp'

        self.smaregiClientId = clientId
        self.smaregiClientSecret = clientSecret
        self._uriInfo = self.uriAccess + 'userinfo'

        self.accessToken = ''
        self.contractId = ''

        self.logger = logger
#        smaregiClientId = getattr(settings, "SMAREGI_CLIENT_ID", None)
#        smaregiClientSecret = getattr(settings, "SMAREGI_CLIENT_SECRET", None)
#        base = base64.b64encode((smaregiClientId+":"+smaregiClientSecret).encode())
#        smaregiAuth = "Basic " + str(base).split("'")[1]

#headers = {
#    'Authorization': smaregiAuth,
#    'Content-Type':	'application/x-www-form-urlencoded',        
#}
#body = {
#    'grant_type':'client_credentials',
#    'scope': ''
#}
#encodedBody = urlencode(body)
#r_post = requests.post(url, headers=headers, data=urlencode(body))
