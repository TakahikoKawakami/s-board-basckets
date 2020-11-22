from urllib.parse import urlencode
from flask import redirect

import base64
import requests
import json
import time
import jwt
import logging
from urllib.parse import urlencode

from .BaseApi import BaseApi

class AuthorizeApi(BaseApi):
    def __init__(self, config, redirectUri):
        super().__init__(config)
        self.redirectUri = redirectUri
        self.csrf = 'rundomStringForProdcution'
        self.uriAuth = self.config.uriAccess + '/authorize'
        self.uriInfo = self.config.uriAccess + '/userinfo'    

    def authorize(self):
        query = {
            'response_type': 'code',
            'client_id': self.config.smaregiClientId,
            'scope': 'openid',
            'state': self.csrf,
            'redirect_uri': self.redirectUri
        }
        params = urlencode(query)
        return redirect(f'{self.uriAuth}?{params}')


    def getUserInfo(self, code, state):
        userAccessToken = self._getUserAccessToken(code)
        accessToken = userAccessToken['access_token']
        infoHeader = {
            'Authorization': 'Bearer ' + accessToken
        }
        
        r_post = requests.post(self.uriInfo, headers=infoHeader).json()
        return r_post
#        token = self._generateJwt(r_post['contract'])
#        tokenDecode = jwt.decode(token, 'secret', algorithm='HS256')
#        return HttpResponse(token)

#        form = LoginForm(request.POST)
#        return render(request, 'login.html', {'form': form,})


    def _getUserAccessToken(self, code):
        base = base64.b64encode((self.config.smaregiClientId + ":" + self.config.smaregiClientSecret).encode())
        smaregiAuth = "Basic " + str(base).split("'")[1]
        headers = {
            'Authorization': smaregiAuth,
            'Content-Type':	'application/x-www-form-urlencoded',        
        }
        body = {
            'grant_type':'authorization_code',
            'code': code,
            'redirect_uri': self.redirectUri,
        }
        encodedBody = urlencode(body)
        result = requests.post(self.uriAuth + '/token', headers=headers, data=urlencode(body))
        result = result.json()
        return result

