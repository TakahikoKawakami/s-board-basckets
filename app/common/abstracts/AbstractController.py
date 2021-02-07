import random
from app import logger

from app.config import templates
from app.common.managers import SessionManager
from app.domains.AccountDomainService import AccountDomainService
from app.domains.StoreDomainService import StoreDomainService

class AbstractController():
    def __init__(self) -> None:
        self._logger = None

        self._loginAccount = None
        self._storeList = []
        self._accountDomainService = None

        self._req = None
        self._resp = None

    async def on_request(self, req, resp):
        self._req = req
        self._resp = resp

        self._accountDomainService = AccountDomainService(resp.session)
        if not self._accountDomainService.hasContractId():
            resp.redirect('/', status_code=303)
            return
        await self._accountDomainService.prepareForAccessProcessing()
        self._loginAccount = self._accountDomainService.loginAccount
        self._logger = await logger.getLogger(self._loginAccount)

        if self._req.method in ("post", "put", "patch"):
            await self._checkCsrfToken()
        
        storeDomainService = StoreDomainService(self._loginAccount)
        self._storeList = await storeDomainService.getStoreList()

    async def render(self, path="/", *args, **kwargs):
        if SessionManager.has(self._resp.session, SessionManager.KEY_ERROR_MESSAGES):
            messages = SessionManager.get(self._resp.session, SessionManager.KEY_ERROR_MESSAGES)
            SessionManager.remove(self._resp.session, SessionManager.KEY_ERROR_MESSAGES)
            kwargs['message'] = messages
        else:
            kwargs['message'] = ""

        storeDomainService = StoreDomainService(self._loginAccount)
        kwargs['displayStore'] = await storeDomainService.getDisplayStore()
        kwargs['stores'] = await storeDomainService.getStoreList()
        kwargs['loginStatus'] = self._loginAccount.loginStatus

        self.createCsrfToken()
        kwargs['csrf_hidden_input'] = self._inputCsrfToken()
        kwargs['csrf_token'] = SessionManager.get(self._resp.session, SessionManager.KEY_CSRF_TOKEN)
        

        self._resp.html = templates.render(path, kwargs)


    def createCsrfToken(self):
        csrfToken = hex(random.getrandbits(64))
        SessionManager.set(self._resp.session, SessionManager.KEY_CSRF_TOKEN, csrfToken)
        return csrfToken

    def _inputCsrfToken(self):
        csrf = SessionManager.get(self._resp.session, SessionManager.KEY_CSRF_TOKEN)
        return '<input type="hidden" name="csrf_token" value="{}">'.format(csrf)

    async def _checkCsrfToken(self):
        self._resp.status_code = 200
        request = await self._req.media()
        if "csrf_token" not in request:
            self._logger.warning('not have csrf_token')
            self._resp.status_code = 401
        if request['csrf_token'] != SessionManager.get(self._resp.session, SessionManager.KEY_CSRF_TOKEN):
            print(request['csrf_token'])
            print(hex(request['csrf_token']))
            print(SessionManager.get(self._resp.session, SessionManager.KEY_CSRF_TOKEN))
            self._logger.warning('invalid csrf_token')
            self._resp.status_code = 401

    def isBookingRedirect(self):
        return self._resp.headers.get('Location') is not None

    def isAccessDenied(self):
        return self._resp.status_code != 200