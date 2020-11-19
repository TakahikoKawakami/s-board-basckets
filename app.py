from flask import Flask, render_template, request, redirect
import settings

"""for smaregi api"""
import json
import base64
import requests
from urllib.parse import urlencode

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    authorize = Authorize()
    return authorize.get()
#    return settings.ENV_DIVISION
#     return render_template('index.html')


@app.route('/accounts/login')
def login():
    loginClass = Login()
    return loginClass.get(request.args.get('code', ''), request.args.get('state', ''))

@app.route('/contact', methods=['POST'])
def contact():
    name = request.json['name']
    email = request.json['email']
    message = request.json['message']
    result = "Success, name: " + name + "email: " + email + "message: " + message
    return result 


class Authorize():
    def __init__(self):
        self._uriAuth = 'https://id.smaregi.dev/authorize'
        self._uriApp = settings.APP_URI
        self._smaregiClientId = settings.SMAREGI_CLIENT_ID
        
        
    def get(self):
        query = {
            'response_type': 'code',
            'client_id': self._smaregiClientId,
            'scope': 'openid',
            'state': 'test',
            'redirect_uri': self._uriApp + 'accounts/login'
        }
        params = urlencode(query)
        redirectUri = f'{self._uriAuth}?{params}'
        return redirect(redirectUri)


#ログイン機能
class Login():
    def __init__(self):
        self._uriAuth = 'https://id.smaregi.dev/authorize/token'
        self._uriInfo = 'https://id.smaregi.dev/userinfo'
        self._uriApp = settings.APP_URI
        
        self._smaregiClientId = settings.SMAREGI_CLIENT_ID
        self._smaregiClientSecret = settings.SMAREGI_CLIENT_SECRET

    def get(self, code, state):
        userAccessToken = self._getUserAccessToken(code)
        accessToken = userAccessToken['access_token']
        infoHeader = {
            'Authorization': 'Bearer ' + accessToken
        }
        
        r_post = requests.post(self._uriInfo, headers=infoHeader).json()
        return r_post
#        token = self._generateJwt(r_post['contract'])
#        tokenDecode = jwt.decode(token, 'secret', algorithm='HS256')
#        return token
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
            'redirect_uri': self._uriApp + 'accounts/login',
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


#app.pyをターミナルから直接呼び出した時だけ、app.run()を実行する
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
