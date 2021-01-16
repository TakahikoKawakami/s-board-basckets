import datetime
from flask import Blueprint, \
                  render_template,\
                  url_for,\
                  request,\
                  redirect,\
                  session

from logging import getLogger

from models import Accounts as models


"""TODO: lib.Smaregiをpip installでimportできるようにする"""
# import sys
# from pathlib import Path
# root_path = str(Path('__file__').resolve().parent.parent.parent)
# sys.path.append(root_path)  # ルートディレクトリを環境変数に一時的に取り込む
from lib.Smaregi.config import config as SmaregiConfig
from lib.Smaregi.API.Authorize import AuthorizeApi


from common.managers import SessionManager

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
    if not ('contract_id' in session):
        return redirect('/')

    contractId = session['contract_id']
    result = authorizeApi.getAccessToken(
        contractId,
        [
            'pos.products:read',
            'pos.transactions:read',
            'pos.stores:read',
        ]
    )

    session['access_token'] = result['access_token']
    session['access_token_expires_in'] = datetime.datetime.now() + datetime.timedelta(seconds=result['expires_in'])
    
    if request.args.get('next') is not None:
        _queryParams = SessionManager.get(SessionManager.KEY_QUERY_PARAMS_FOR_REDIRECT)
        _queryString = '?'
        for _query, _value in _queryParams.items():
            _queryString += _query + "=" + _value + "&"
        _queryString = _queryString.rstrip("&")

        SessionManager.remove(SessionManager.KEY_QUERY_PARAMS_FOR_REDIRECT)

        return redirect(request.args.get('next') + _queryString)
        

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
    return redirect(url_for('baskets.index'))


@route.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')


@route.route('/webhook')
def webhook():
    print('webhook!!!')
    return '', 200