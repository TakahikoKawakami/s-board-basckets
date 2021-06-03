from app.common.abstracts.AbstractController import AbstractController
from app.domains.StoreDomainService import StoreDomainService


class AccountStore(AbstractController):
    def __init__(self) -> None:
        super().__init__()

    async def on_get(self, req, resp):
        self._logger.info('get AccountStore')
        store_domain_service = StoreDomainService(self.login_account)
        store_list = await store_domain_service.get_store_list()

        json_encoded = []
        for store in store_list:
            json_encoded.append(await store.serialize)

        resp.media = json_encoded
        return
        
    async def on_put(self, req, resp):
        self._logger.info('put AccountStore')
        try:
            store_domain_service = StoreDomainService(self.login_account)
            await store_domain_service.delete_all_stores()
            await store_domain_service.sync_all_stores()

            resp.media = {
                "status": 200
   	        }
        except Exception as e:
            self._logger.exception('raise error: %s', e)
            resp.media = {
                "status": 500
   	        }
        return

class AccountSetting(AbstractController):
    def __init__(self) ->None:
        super().__init__()

    async def on_get(self, req, resp):
        self._logger.info('get AccountSetting')
        account_setting = await self.login_account.account_setting_model
        json_encoded = await account_setting.serialize
        resp.media = json_encoded
        return
        
    async def on_post(self, req, resp):
        self._logger.info('post AccountSetting')
        request = await req.media()
        await self._account_domain_service.save_account_setting(request)
        resp.media = {
            "status": 200
        }
        return
        # self._basketDomainService = BasketDomainService(self._loginAccount)
        # nowMonth = datetime.datetime.now().month
        # dailyBasketList = await self._basketDomainService.getDailyBasketListByMonth(nowMonth)
