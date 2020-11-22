from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.views import View

# from .models import Book
# from .forms import *
import base64
import requests
from urllib.parse import urlencode
import json
# from .models import Accounts
from . forms import LoginForm

import time
import jwt

import logging
from .serializer import AccountSerializer
from rest_framework import viewsets, filters
from django.views.decorators.csrf import csrf_exempt


#ログイン機能
class Login(View):
    def __init__(self):
        self._uriAuth = 'https://id.smaregi.dev/authorize/token'
        self._uriInfo = 'https://id.smaregi.dev/userinfo'
        self._uriApp = getattr(settings, "APP_URI", None)
        
        self._smaregiClientId = getattr(settings, "SMAREGI_CLIENT_ID", None)
        self._smaregiClientSecret = getattr(settings, "SMAREGI_CLIENT_SECRET", None)

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        state = request.GET.get('state')
    
        userAccessToken = self._getUserAccessToken(code)
        accessToken = userAccessToken['access_token']
        infoHeader = {
            'Authorization': 'Bearer ' + accessToken
        }
        
        r_post = requests.post(self._uriInfo, headers=infoHeader).json()
        token = self._generateJwt(r_post['contract'])
        tokenDecode = jwt.decode(token, 'secret', algorithm='HS256')
        return HttpResponse(token)
#        form = LoginForm(request.POST)
#        return render(request, 'login.html', {'form': form,})


    def _getUserAccessToken(self, code):
        base = base64.b64encode((self._smaregiClientId + ":" + self._smaregiClientSecret).encode())
        smaregiAuth = "Basic " + str(base).split("'")[1]
        headers = {
            'Authorization': smaregiAuth,
            'Content-Type':	'application/x-www-form-urlencoded',        
        }
        body = {
            'grant_type':'authorization_code',
            'code': code,
            'redirect_uri': self._uriApp + 'accounts/login/',
        }
        encodedBody = urlencode(body)
        result = requests.post(self._uriAuth, headers=headers, data=urlencode(body))
        result = result.json()
        return result
        
    
    
    def _generateJwt(self, contractData):
        key = 'secret'
        # encoded = jwt.encode({'some': 'payload'}, key, algorithm='HS256')
        # 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg'
        # decoded = jwt.decode(encoded, key, algorithms='HS256')
        # {'some': 'payload'}
        # try:
        #     jwt.decode('JWT_STRING', 'secret', algorithms=['HS256'])
        # except jwt.ExpiredSignatureError:
        #     # Signature has expired
        # jwtライブラリでTokenを生成します
        # Tokenの内容はユーザーの情報とタイムアウトが含まれてます
        # タイムアウトのキーはexpであることは固定してます
        # ドキュメント: https://pyjwt.readthedocs.io/en/latest/usage.html?highlight=exp
        timestamp = int(time.time()) + 60*60*24*7
        return jwt.encode(
            {"id": contractData['id'], "is_owner": contractData['is_owner'], "exp": timestamp},
            key,
            algorithm='HS256'
        )

    
class Authorize(View):
    def __init__(self):
        self._uriAuth = 'https://id.smaregi.dev/authorize'
        self._uriApp = getattr(settings, "APP_URI", None)
        self._smaregiClientId = getattr(settings, "SMAREGI_CLIENT_ID", None)
        
        
    def get(self, request):
        query = {
            'response_type': 'code',
            'client_id': self._smaregiClientId,
            'scope': 'openid',
            'state': 'test',
            'redirect_uri': self._uriApp + 'accounts/login/'
        }
        params = urlencode(query)
        redirectUri = f'{self._uriAuth}?{params}'
        return redirect(redirectUri)


class SignUp(View):
    def post(self, request, *arg, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
#            username = form.cleaned_data.get('username')
            user = Accounts.objects.get(name=username)
            login(request, user)
            # return redirect('/')
        return render(request, 'login.html', {'form': form,})           


@csrf_exempt
def sign_up(request):
    logger = logging.getLogger('file')
    #header = json.loads(request.header)
    data = json.loads(request.body)
    logger.info(data)
    #logger.info(header)


# Create your views here.
def getSmaregiAccessToken(request):
    """get access token for smaregi"""
    contractId = 'sb_skc130x6'
    url = 'https://id.smaregi.dev/app/' + contractId + '/token'

    smaregiClientId = getattr(settings, "SMAREGI_CLIENT_ID", None)
    smaregiClientSecret = getattr(settings, "SMAREGI_CLIENT_SECRET", None)

    base = base64.b64encode((smaregiClientId+":"+smaregiClientSecret).encode())
    smaregiAuth = "Basic " + str(base).split("'")[1]
    headers = {
        'Authorization': smaregiAuth,
        'Content-Type':	'application/x-www-form-urlencoded',        
    }
    body = {
        'grant_type':'client_credentials',
        'scope': ''
    }
    encodedBody = urlencode(body)
    r_post = requests.post(url, headers=headers, data=urlencode(body))
    r_post = r_post.json()


    return HttpResponse(r_post["access_token"])
    # return render(request, 's_board_relations/network.html')
