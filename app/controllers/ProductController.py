import datetime
from flask import Blueprint, \
                  render_template,\
                  url_for,\
                  request,\
                  redirect,\
                  session

import logging


from lib.Smaregi.config import config as SmaregiConfig
from lib.Smaregi.API.Authorize import AuthorizeApi

from config import AppConfig

appConfig = AppConfig()
apiConfig = SmaregiConfig(
    appConfig.ENV_DIVISION,
    appConfig.SMAREGI_CLIENT_ID,
    appConfig.SMAREGI_CLIENT_SECRET
)
authorizeApi = AuthorizeApi(apiConfig, appConfig.APP_URI + '/accounts/login')

route = Blueprint('accounts', __name__, url_prefix='/accounts')



class ProductController():
    def __init__(self, api):
        self.smaregiApi = api
    
    def network(request):
        """network"""
        url = 'https://id.smaregi.dev/app/sb_skc130x6/token'
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
    #    return HttpResponse(r_post["access_token"])
        return render(request, 's_board_relations/network.html')
