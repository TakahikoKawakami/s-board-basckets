import datetime
from flask import Blueprint, \
                  render_template,\
                  url_for,\
                  request,\
                  redirect,\
                  session

from logging import getLogger

from ..models import Accounts as models


"""TODO: lib.Smaregiをpip installでimportできるようにする"""
# import sys
# from pathlib import Path
# root_path = str(Path('__file__').resolve().parent.parent.parent)
# sys.path.append(root_path)  # ルートディレクトリを環境変数に一時的に取り込む
from lib.Smaregi.config import config as SmaregiConfig
from lib.Smaregi.API.Authorize import AuthorizeApi

from config import AppConfig
from factories.ModelFactory import ModelFactory

appConfig = AppConfig()
modelFactory = ModelFactory(appConfig)

apiConfig = SmaregiConfig(
    appConfig.ENV_DIVISION,
    appConfig.SMAREGI_CLIENT_ID,
    appConfig.SMAREGI_CLIENT_SECRET
)
authorizeApi = AuthorizeApi(apiConfig, appConfig.APP_URI + '/accounts/login')

route = Blueprint('accounts', __name__, url_prefix='/accounts')

logger = getLogger('flask.app')

@route.route('/authorize', methods=['GET'])
def authorize():
    logger.debug('authorize')
    return authorizeApi.authorize()


@route.route('/token', methods=['GET'])
def getToken():
    contractId = session['contract_id']
    result = authorizeApi.getAccessToken(
        contractId,
        [
            'pos.products:read',
            'pos.transactions:read'
        ]
    )
    print(result)

    session['access_token'] = result['access_token']
    session['access_token_expires_in'] = datetime.datetime.now() + datetime.timedelta(seconds=result['expires_in'])
    
    if request.args.get('next') is not None:
        return redirect(request.args.get('next'))
        

@route.route('/login', methods=['GET'])
def login():
    logger.info('login!!!')
    code = request.args.get('code')
    state = request.args.get('state')

    logger.info('code: {code}, state: {state}')
    if (code is None or state is None):
        return redirect('/accounts/authorize')

    result = authorizeApi.getUserInfo(code, state)
    
    requestContractId = result['contract']['id']
    accountModel = modelFactory.createAccount()
    account = accountModel.showByContractId(requestContractId)
    if (account is None):
        accountModel.contractId = requestContractId
        accountModel.status = 'start'
        registeredAccount = accountModel.register()
    
    session['contract_id'] = requestContractId
    return redirect('/')


@route.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')


@route.route('', methods=['GET', 'POST'])
def test():
    try:
        if request.method == 'GET': # login
            accountModel = modelFactory.createAccount()

            if ('contract_id' in session):
                account = accountModel.showByContractId(session['contract_id'])
                if (account != None):
                    return 'logined ' + account.contract_id
                else:
                    session.pop['contract_id']
                    return 'session failed ?'
            else:
                _contractId = request.args.get('contract_id', '')
                account = accountModel.showByContractId(_contractId)
                if (account != None):
                    session['contract_id'] = _contractId
                    return 'set'
                else:
                    return 'who?'
        elif request.method == 'POST':
            accountModel = modelFactory.createAccount()
            _contractId = request.form['contract_id']
            _status = request.form['status']

            accountModel.contractId = _contractId
            accountModel.status = _status

            registeredAccount = accountModel.register()
            return redirect(url_for('home.index'))
        else:
            return abort(400)
    except Exception as e:
        return str(e)
        

@route.route('delete', methods=['POST'])
def testDelete():
    try:
        if request.method == 'POST':
            contractId = request.form['contract_id']
            accountmodel = modelFactory.createAccount()
            account = accountModel.showByContractId(contractId)
            
            if (account == None):
                return 'non type error'
            account.delete()
            return redirect('/')
        else:
            return abort(400)
    except Exception as e:
        return str(e)
        


