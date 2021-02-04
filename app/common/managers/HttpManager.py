import responder
from app.config import templates
from app.models import Store, Account
from app.domains.StoreDomainService import StoreDomainService

def isBookingRedirect(resp):
    return resp.headers.get('Location') is not None

async def render(resp: responder.models.Response, account: Account, path="/", messages="", *args, **kwargs):
    storeDomainService = StoreDomainService(account)
    kwargs['message'] = messages
    kwargs['displayStore'] = await storeDomainService.getDisplayStore()
    kwargs['stores'] = await storeDomainService.getStoreList()

    resp.html =  templates.render(path, kwargs)