class config():
    ENV_DIVISION_LOCAL = 'LOCAL'
    ENV_DIVISION_STAGING = 'STAGING'
    ENV_DIVISION_PRODUCTION = 'PROD'
    
    def __init__(self, env_division, clientId, clientSecret):
        if (env_division == self.ENV_DIVISION_LOCAL) or (env_division == self.ENV_DIVISION_STAGING):
            self.uriAccess = 'https://id.smaregi.dev' # app/sb_skc130x6/token'            
            self.uriApi = 'https://api.smaregi.dev'            
        else:
            self.uriAccess = 'https://id.smaregi.jp'
            self.uriApi = 'https://api.smaregi.jp'

        self.smaregiClientId = clientId
        self.smaregiClientSecret = clientSecret        
        self._uriInfo = self.uriAccess + 'userinfo'            
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
