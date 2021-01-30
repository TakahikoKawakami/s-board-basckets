from app.logger import ApplicationLogger
from app.domains.AccountsDomainService import AccountsDomainService

class AbstractController():
    def __init__(self) -> None:
        self._logger = None

        self._loginAccount = None
        self._accountsDomainService = None

    async def on_request(self, req, resp):
        self._accountsDomainService = AccountsDomainService(resp.session)
        if not self._accountsDomainService.hasContractId():
            resp.redirect('/', status_code=303)
            return
        await self._accountsDomainService.prepareForAccessProcessing()
        self._loginAccount = self._accountsDomainService.loginAccount
        self._logger = ApplicationLogger(self._loginAccount)