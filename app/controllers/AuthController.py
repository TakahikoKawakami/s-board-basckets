import datetime
from logging import getLogger

from app.models import Accounts as models

"""TODO: lib.Smaregiをpip installでimportできるようにする"""
# import sys
# from pathlib import Path
# root_path = str(Path('__file__').resolve().parent.parent.parent)
# sys.path.append(root_path)  # ルートディレクトリを環境変数に一時的に取り込む
from app.lib.Smaregi.config import config as SmaregiConfig
from app.lib.Smaregi.API.Authorize import AuthorizeApi


from app.common.managers import SessionManager
from app.common.utils import DictionaryUtil
from app.domains.AccountsDomainService import AccountsDomainService

from app.config import AppConfig

appConfig = AppConfig()

apiConfig = SmaregiConfig(
    appConfig.ENV_DIVISION,
    appConfig.SMAREGI_CLIENT_ID,
    appConfig.SMAREGI_CLIENT_SECRET
)
authorizeApi = AuthorizeApi(apiConfig, appConfig.APP_URI + '/accounts/login')

logger = getLogger('flask.app')


# @route.route('/authorize', methods=['GET'])
def authorize(req, resp):
    logger.debug('authorize')
    resp.redirect(authorizeApi.authorize())


# @route.route('/token', methods=['GET'])
def getToken(req, resp):
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

    SessionManager.set(SessionManager.KEY_ACCESS_TOKEN, result.accessToken)
    SessionManager.set(SessionManager.KEY_ACCESS_TOKEN_EXPIRES_IN, result.expirationDateTime)
    
    if request.args.get('next') is not None:
        _queryParams = SessionManager.get(SessionManager.KEY_QUERY_PARAMS_FOR_REDIRECT)
        _queryString = '?'
        for _query, _value in _queryParams.items():
            _queryString += _query + "=" + _value + "&"
        _queryString = _queryString.rstrip("&")

        SessionManager.remove(SessionManager.KEY_QUERY_PARAMS_FOR_REDIRECT)

        return redirect(request.args.get('next') + _queryString)
        

async def login(req, resp):
    logger.info('login!!!')
    code = DictionaryUtil.getByKey('code', req.params)
    state = DictionaryUtil.getByKey('state', req.params)

    logger.info('code: {code}, state: {state}')
    if (code is None or state is None):
        resp.redirect('/accounts/authorize')
        return

    accountsDomainService = AccountsDomainService(req.session).withSmaregiApi(None, None)
    account = await accountsDomainService.loginByCodeAndState(code, state)
    
    SessionManager.set(resp.session, SessionManager.KEY_CONTRACT_ID, account.contractId)
    resp.redirect('/baskets/associate')
    return


def logout(req, resp):
    resp.session.clear()
    resp.redirect('/')
    return

