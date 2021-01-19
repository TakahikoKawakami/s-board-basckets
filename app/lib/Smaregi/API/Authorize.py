from urllib.parse import urlencode
import datetime

import requests
import json
import time
import logging

from .BaseIdentificationApi import BaseIdentificationApi
from ..entities.Authorize import *

class AuthorizeApi(BaseIdentificationApi):
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
        return f'{self.uriAuth}?{params}'
        # return redirect(f'{self.uriAuth}?{params}')


    def getUserInfo(self, code, state):
        userAccessToken = self._getUserAccessToken(code)
        accessToken = userAccessToken.accessToken
        infoHeader = {
            'Authorization': 'Bearer ' + accessToken
        }
        
        r_post = requests.post(self.uriInfo, headers=infoHeader).json()
        return UserInfo(r_post)


    def getAccessToken(self, contractId, scopeList):
        url = self.config.uriAccess + '/app/' + contractId + '/token'
        headers = self._getHeader()
        scopeString = " ".join(scopeList)
        body = {
            'grant_type':'client_credentials',
            'scope': scopeString
        }
        r_post = requests.post(url, headers=headers, data=urlencode(body))
        r_post = r_post.json()
        return AccessToken(r_post['access_token']['expires_in'])
        # return r_post
    #    return render(request, 's_board_relations/network.html')


    def _getUserAccessToken(self, code):
        headers = self._getHeader()
        body = {
            'grant_type':'authorization_code',
            'code': code,
            'redirect_uri': self.redirectUri,
        }
        encodedBody = urlencode(body)
        result = requests.post(self.uriAuth + '/token', headers=headers, data=urlencode(body))
        result = result.json()
        return UserAccessToken(result['access_token'])

