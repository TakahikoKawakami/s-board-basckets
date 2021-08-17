from smaregipy import SmaregiPy
from smaregipy.account import Account

from app.common.managers import SessionManager
from app.domains.AccountDomainService import AccountDomainService

from app.config import AppConfig


app_config = AppConfig()
SmaregiPy.init_by_dict({
    'env_division': AppConfig.ENV_DIVISION,
    'smaregi_client_id': AppConfig.SMAREGI_CLIENT_ID,
    'smaregi_client_secret': AppConfig.SMAREGI_CLIENT_SECRET,
    'redirect_uri': AppConfig.APP_URI + '/accounts/login'
})


def authorize(req, resp):
    resp.redirect(Account.authentication_uri())


async def login(req, resp):
    code = req.params.get('code')
    state = req.params.get('state')

    if (code is None or state is None):
        resp.redirect('/accounts/authorize', status_code=303)
        return

    account_domain_service = AccountDomainService(req.session)
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
