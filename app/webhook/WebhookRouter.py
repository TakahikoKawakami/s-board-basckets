import responder
# from app.webhook import TransactionsWebhook

EVENT_TRANSACTIONS = 'pos:transactions'

def recieved(header, body):
    _contractId = header['smaregi-contract-id']
    _event = header['smaregi-event']
    # if (_event == EVENT_TRANSACTIONS):
        # TransactionsWebhook.received(_contractId, _event, body)
