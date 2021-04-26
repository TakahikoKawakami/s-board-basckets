from app.lib.Smaregi.API.POS.entities import TransactionHead, TransactionDetail

class Transaction():
    """取引entity
    """
    def __init__(self, head: 'TransactionHead', details: list['TransactionDetail']):
        self.head = head
        self.details = details
