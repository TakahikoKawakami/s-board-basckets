import logging

from app.domains.AccountsDomainService import AccountsDomainService

class AbstractController():
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)

        self._loginAccount = None
        self._accountsDomainService = None

    async def on_request(self, req, resp):
        self._accountsDomainService = AccountsDomainService(resp.session)
        if not self._accountsDomainService.hasContractId():
            resp.redirect('/', status_code=303)
            return
        await self._accountsDomainService.prepareForAccessProcessing()
        self._loginAccount = self._accountsDomainService.loginAccount