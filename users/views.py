from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views import View

# from .models import Book
# from .forms import *
import base64
import requests
from urllib.parse import urlencode
import json
from .models import Accounts
from . forms import LoginForm


#ログイン機能
class Login(View):
    def post(self, request, *arg, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = Accounts.objects.get(name=username)
            login(request, user)
            # return redirect('/')
        return render(request, 'login.html', {'form': form,})

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        return render(request, 'login.html', {'form': form,})

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