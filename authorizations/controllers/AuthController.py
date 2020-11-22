from flask import Blueprint, \
                  render_template,\
                  url_for,\
                  request,\
                  redirect,\
                  session

import logging

from ..models import Accounts as models


"""TODO: lib.Smaregiをpip installでimportできるようにする"""
# import sys
# from pathlib import Path
# root_path = str(Path('__file__').resolve().parent.parent.parent)
# sys.path.append(root_path)  # ルートディレクトリを環境変数に一時的に取り込む
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

@route.route('/authorize', methods=['GET'])
def authorize():
    return authorizeApi.authorize()


@route.route('/login', methods=['GET'])
def login():
    code = request.args.get('code')
    state = request.args.get('state')
    result = authorizeApi.getUserInfo(code, state)
    
    requestContractId = result['contract']['id']
    account = models.showByContractId(requestContractId)
    if (account is None):
        account = models.Account(requestContractId, 'start')
        registeredAccount = account.register()
    
    session['contract_id'] = result['contract']['id']
    return session['contract_id']


@route.route('', methods=['GET', 'POST'])
def test():
    try:
        if request.method == 'GET': # login
            if ('contract_id' in session):
                account = models.showByContractId(session['contract_id'])
                if (account != None):
                    return 'logined ' + account.contract_id
                else:
                    session.pop['contract_id']
                    return 'session failed ?'
            else:
                _contractId = request.args.get('contract_id', '')
                account = models.showByContractId(_contractId)
                if (account != None):
                    session['contract_id'] = _contractId
                    return 'set'
                else:
                    return 'who?'
        elif request.method == 'POST':
            _contractId = request.form['contract_id']
            _status = request.form['status']
            account = models.Account(_contractId, _status)
            registeredAccount = account.register()
            return redirect(url_for('route.index'))
        else:
            return abort(400)
    except Exception as e:
        return str(e)
        

@route.route('delete', methods=['POST'])
def testDelete():
    try:
        if request.method == 'POST':
            contractId = request.form['contract_id']
            account = models.showByContractId(contractId)
            if (account == None):
                return 'non type error'
            account.delete()
            return redirect('/')
        else:
            return abort(400)
    except Exception as e:
        return str(e)
        


