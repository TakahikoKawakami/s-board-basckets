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

#ログイン機能
class Login(View):
    def post(self, request, *arg, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
#            username = form.cleaned_data.get('username')
            user = Accounts.objects.get(name=username)
            login(request, user)
            # return redirect('/')
        return render(request, 'login.html', {'form': form,})

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        state = request.GET.get('state')
        url = 'https://id.smaregi.dev/authorize/token'
        smaregiClientId = getattr(settings, "SMAREGI_CLIENT_ID", None)
        smaregiClientSecret = getattr(settings, "SMAREGI_CLIENT_SECRET", None)
    
        base = base64.b64encode((smaregiClientId+":"+smaregiClientSecret).encode())
        smaregiAuth = "Basic " + str(base).split("'")[1]
        headers = {
            'Authorization': smaregiAuth,
            'Content-Type':	'application/x-www-form-urlencoded',        
        }
        body = {
            'grant_type':'authorization_code',
            'code': code,
            'redirect_uri': 'http://127.0.0.1:8000/users/login',
        }
        encodedBody = urlencode(body)
        r_post = requests.post(url, headers=headers, data=urlencode(body))
        r_post = r_post.json()
        
        infoUrl = 'https://id.smaregi.dev/userinfo'
        accessToken = r_post['access_token']
        infoHeader = {
            'Authorization': 'Bearer ' + accessToken
        }
        
        r_post = requests.post(infoUrl, headers=infoHeader).json()
        token = self._generateJwt(r_post['contract'])
        return HttpResponse(r_post['contract'])
#        form = LoginForm(request.POST)
#        return render(request, 'login.html', {'form': form,})
    
    
    def _generateJwt(self, contractData):
        # 先程インストールしたjwtライブラリでTokenを生成します
        # Tokenの内容はユーザーの情報とタイムアウトが含まれてます
        # タイムアウトのキーはexpであることは固定してます
        # ドキュメント: https://pyjwt.readthedocs.io/en/latest/usage.html?highlight=exp
        timestamp = int(time.time()) + 60*60*24*7
        return jwt.encode(
            {"id": contractData['id'], "is_owner": contractData['is_owner'], "exp": timestamp},
            SECRET_KEY
        ).decode("utf-8")

login = Login.as_view()

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
    
    
class LoginBata(View):
    def get(self, request):
        authorizeUrl = 'http://id.smaregi.dev/authorize'
        smaregiClientId = getattr(settings, "SMAREGI_CLIENT_ID", None)
        query = {
            'response_type': 'code',
            'client_id': smaregiClientId,
            'scope': 'openid',
            'state': 'test',
            'redirect_uri': 'http://127.0.0.1:8000/users/login',
        }
        params = urlencode(query)
        authorizeUrl = f'{authorizeUrl}?{params}'
        return redirect(authorizeUrl)
