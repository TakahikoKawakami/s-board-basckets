from smaregipy.entities.transaction import HeadEntity, DetailEntity


class Transaction():
    """取引entity
    """
    def __init__(self, head: 'HeadEntity', details: list['DetailEntity']):
        self.head = head
        self.details = details
