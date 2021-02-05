import responder
from app.common.managers import SessionManager
from app.config import templates
from app.models import Store, Account
from app.domains.StoreDomainService import StoreDomainService

def isBookingRedirect(resp):
    return resp.headers.get('Location') is not None

async def render(resp:responder.models.Response, account:Account, path="/", *args, **kwargs):
    if SessionManager.has(resp.session, SessionManager.KEY_ERROR_MESSAGES):
        messages = SessionManager.get(resp.session, SessionManager.KEY_ERROR_MESSAGES)
        SessionManager.remove(resp.session, SessionManager.KEY_ERROR_MESSAGES)
        kwargs['message'] = messages
    else:
        kwargs['message'] = ""

    storeDomainService = StoreDomainService(account)
    kwargs['displayStore'] = await storeDomainService.getDisplayStore()
    kwargs['stores'] = await storeDomainService.getStoreList()

    resp.html =  templates.render(path, kwargs)