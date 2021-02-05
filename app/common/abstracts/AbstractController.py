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

        self._resp.html =  templates.render(path, kwargs)