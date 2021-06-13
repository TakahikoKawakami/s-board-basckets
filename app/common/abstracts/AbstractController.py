import random
from app import logger

from app.config import templates
import app.common.managers.SessionManager as SessionManager
from app.domains.AccountDomainService import AccountDomainService
from app.domains.StoreDomainService import StoreDomainService


class AbstractController():
    def __init__(self) -> None:
        self._logger = None

        self.login_account = None
        self._store_list = []
        self._account_domain_service = None

        self._req = None
        self._resp = None

    async def on_request(self, req, resp):
        self._req = req
        self._resp = resp

        self._account_domain_service = AccountDomainService(resp.session)
        if not self._account_domain_service.has_contract_id():
            resp.redirect('/', status_code=303)
            return
        await self._account_domain_service.prepare_for_access_processing()
        self.login_account = self._account_domain_service.login_account
        self._logger = await logger.get_logger(self.login_account.contract_id)
        self._logger.contract_id = self.login_account.contract_id

        if self._req.method in ("post", "put", "patch"):
            await self._check_csrf_token()

        store_domain_service = StoreDomainService(self.login_account)
        self._store_list = await store_domain_service.get_store_list()

    async def render(self, path="/", *args, **kwargs):
        if SessionManager.has(self._resp.session, SessionManager.KEY_ERROR_MESSAGES):
            messages = SessionManager.get(self._resp.session, SessionManager.KEY_ERROR_MESSAGES)
            SessionManager.remove(self._resp.session, SessionManager.KEY_ERROR_MESSAGES)
            kwargs['message'] = messages
        else:
            kwargs['message'] = ""

        account_setting = await self.login_account.account_setting_model
        kwargs['useSmaregiWebhook'] = account_setting.use_smaregi_webhook
        store_domain_service = StoreDomainService(self.login_account)
        kwargs['displayStore'] = await store_domain_service.get_display_store()
        kwargs['stores'] = await store_domain_service.get_store_list()

        kwargs['signUp'] = SessionManager.has(self._resp.session, SessionManager.KEY_SIGN_UP)
        kwargs['signIn'] = self.login_account.login_status == self.login_account.LoginStatusEnum.SIGN_IN
        kwargs['signOn'] = self.login_account.login_status == self.login_account.LoginStatusEnum.SIGN_ON
        SessionManager.remove(self._resp.session, SessionManager.KEY_SIGN_UP)

        self.create_csrf_token()
        kwargs['csrf_hidden_input'] = self._input_csrf_token()
        kwargs['csrf_token'] = SessionManager.get(self._resp.session, SessionManager.KEY_CSRF_TOKEN)

        self._resp.html = templates.render(path, kwargs)

    def create_csrf_token(self):
        csrf_token = hex(random.getrandbits(64))
        SessionManager.set(self._resp.session, SessionManager.KEY_CSRF_TOKEN, csrf_token)
        return csrf_token

    def _input_csrf_token(self):
        csrf = SessionManager.get(self._resp.session, SessionManager.KEY_CSRF_TOKEN)
        return '<input type="hidden" name="csrf_token" value="{}">'.format(csrf)

    async def _check_csrf_token(self):
        self._resp.status_code = 200
        request = await self._req.media()
        if "csrf_token" not in request:
            self._logger.warning('not have csrf_token')
            self._resp.status_code = 401
        if request['csrf_token'] != SessionManager.get(self._resp.session, SessionManager.KEY_CSRF_TOKEN):
            print(request['csrf_token'])
            print(SessionManager.get(self._resp.session, SessionManager.KEY_CSRF_TOKEN))
            self._logger.warning('invalid csrf_token')
            self._resp.status_code = 401

    def is_booking_redirect(self):
        return self._resp.headers.get('Location') is not None

    def is_access_denied(self):
        return self._resp.status_code != 200
