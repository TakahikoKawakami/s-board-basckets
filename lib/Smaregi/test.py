from config import config
from API.Authorize import AuthorizeApi

config = config('LOCAL', 'clientId', 'clientSecret')
api = AuthorizeApi(config)

print(api.authorize('test'))

'accounts/login/'
