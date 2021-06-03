from logging import getLogger
from SmaregiPlatformApi.config import Config as SmaregiConfig
from SmaregiPlatformApi.authorize import AuthorizeApi


from app.common.managers import SessionManager
from app.domains.AccountDomainService import AccountDomainService

from app.config import AppConfig


appConfig = AppConfig()

apiConfig = SmaregiConfig(
    appConfig.ENV_DIVISION,
    appConfig.SMAREGI_CLIENT_ID,
    appConfig.SMAREGI_CLIENT_SECRET
)
authorizeApi = AuthorizeApi(apiConfig, appConfig.APP_URI + '/accounts/login')

logger = getLogger('flask.app')


def authorize(req, resp):
    logger.debug('authorize')
    resp.redirect(authorizeApi.authorize())


async def login(req, resp):
    logger.info('login!!!')
    code = req.params.get('code')
    state = req.params.get('state')

    logger.info('code: {code}, state: {state}')
    if (code is None or state is None):
        resp.redirect('/accounts/authorize', status_code=303)
        return

    account_domain_service = \
        AccountDomainService(req.session).with_smaregi_api(None, None)
    try:
        account = await account_domain_service.login_by_code_and_state(
            code,
            state
        )
    except Exception:
        resp.redirect('/', status_code=302)
        return

    SessionManager.set(
        resp.session,
        SessionManager.KEY_CONTRACT_ID,
        account.contract_id
    )
    if account.login_status == account.LoginStatusEnum.SIGN_UP:
        SessionManager.set(resp.session, SessionManager.KEY_SIGN_UP, True)
    resp.redirect('/baskets', status_code=303)
    return


async def logout(req, resp):
    resp.session.clear()
    resp.redirect('/', status_code=303)
    return
