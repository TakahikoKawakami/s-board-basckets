import responder
import asyncio

from app.config import backgroundQueue
from app import webhook
from app.common.abstracts.AbstractController import AbstractController
class Webhook(AbstractController):
    EVENT_TRANSACTIONS = 'pos:transactions'

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
        _contractId = header['smaregi-contract-id']
        _event = header['smaregi-event']
        if (_event == cls.EVENT_TRANSACTIONS):
            await webhook.TransactionsWebhook().received(_contractId, _event, body)

