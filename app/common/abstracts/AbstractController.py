from app.logger import ApplicationLogger
from app.domains.AccountDomainService import AccountDomainService
from app.domains.StoreDomainService import StoreDomainService

class AbstractController():
    def __init__(self) -> None:
        self._logger = None

        self._loginAccount = None
        self._storeList = []
        self._accountDomainService = None

    async def on_request(self, req, resp):
        self._accountDomainService = AccountDomainService(resp.session)
        if not self._accountDomainService.hasContractId():
            resp.redirect('/', status_code=303)
            return
        await self._accountDomainService.prepareForAccessProcessing()
        self._loginAccount = self._accountDomainService.loginAccount
        self._logger = ApplicationLogger(self._loginAccount)

        storeDomainService = StoreDomainService(self._loginAccount)
        self._storeList = await storeDomainService.getStoreList()