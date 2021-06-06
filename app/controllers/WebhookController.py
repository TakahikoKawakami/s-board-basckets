import asyncio


from app import webhook
from app.common.abstracts.AbstractController import AbstractController
from app.domains.AccountDomainService import AccountDomainService

class Webhook(AbstractController):
    EVENT_TRANSACTIONS = 'pos:transactions'
    EVENT_GET_TRANSACTION_DETAIL_LIST = 'get_transaction_detail_list'
    EVENT_APP_SUBSCRIPTION = 'AppSubscription'

    async def on_post(self, req, resp):
        # @backgroundQueue.task
        # async def receivedWebhook(_header, _body):
        #     await Webhook.router(_header, _body)
        _header = req.headers
        _body = await req.media()

        loop = asyncio.get_event_loop()
        loop.create_task(Webhook.router(_header, _body))
        # await receivedWebhook(_header, _body)
        print('recieve')
        resp.status_code = 200

    @classmethod
    async def router(cls, header, body):
        # 通常のwebhookではなく、callbackの場合
        if body.get('proc_name') is not None:
            _contract_id = body.get('state').get('contractId')
            _event = body.get('proc_name')
        else:
            _contract_id = header['smaregi-contract-id']
            _event = header['smaregi-event']
        
        _account_domain_service = AccountDomainService(None)
        await _account_domain_service.login_by_contract_id(_contract_id)
        _access_account = _account_domain_service.login_account

        if (_event == cls.EVENT_APP_SUBSCRIPTION):
            accounts_webhook = await webhook.AccountsWebhook.create_instance(None)
            await accounts_webhook.received(_event, body)
            return

        if (_event == cls.EVENT_GET_TRANSACTION_DETAIL_LIST):
            transactions_webhook = await webhook.TransactionsWebhook.create_instance(_access_account)
            await transactions_webhook.callback(_event, body)
            return
        
        _account_setting = await _access_account.account_setting_model
        if not _account_setting.use_smaregi_webhook:
            return

        if (_event == cls.EVENT_TRANSACTIONS):
            transactions_webhook = await webhook.TransactionsWebhook.create_instance(_access_account)
            await transactions_webhook.received(_event, body)
            return
