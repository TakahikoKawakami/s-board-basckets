from tortoise import fields
from datetime import datetime

from app.common.abstracts.AbstractTortoiseModel import AbstractTortoiseModel
import app.database as db


class Account(AbstractTortoiseModel):
    """
    アカウントモデル
    """
    STATUS_START = 'start'
    STATUS_STOP = 'stop'

    contract_id = fields.CharField(max_length=32)
    access_token = fields.CharField(max_length=128)
    expiration_date_time = fields.DatetimeField()
    status = fields.CharField(max_length=16)
    test = fields.CharField(max_length=32)

    class Meta:
        abstract=False
        table="accounts"


    #初期化
    def __init__(self):
        pass

    def __repr__(self):
        return "Account<{}, {}, {}>".format(self.id, self.contract_id, self.status)

    @property
    def contractId(self):
        return self.contract_id

    @contractId.setter
    def contractId(self, contractId):
        self.contract_id = contractId

    @property
    def accessToken(self):
        return self.access_token

    @accessToken.setter
    def accessToken(self, accessToken):
        self.access_token = accessToken

    @property
    def expirationDatetime(self):
        return self.expiration_date_time

    @expirationDatetime.setter
    def expirationDatetime(self, expirationDatetime):
        self.expiration_date_time = expirationDatetime

    @classmethod
    def create(cls, contractId, accessToken):
        kwargs = {
            'contract_id': contractId,
            'access_token': accessToken.accessToken,
            'expiration_date_time': accessToken.expirationDatetime,
            'status': cls.STATUS_START,
        }
        
        return super().create(
            contract_id = contractId,
            access_token = accessToken.accessToken,
            expiration_date_time = accessToken.expirationDatetime,
            status = cls.STATUS_START
        )


    def showByContractId(self, _contractId):
        account = db.session.query(Account).filter(Account.contract_id == _contractId).first()
        return account
#    return Account(account.contract_id, account.status)


class MockAccount():
    def __init__(self):
        pass

    @property
    def contractId(self, contractId):
        pass

    
    @property
    def status(self, status):
        pass


    def register(self):
        return self


    def delete(self):
        return self


    def showByContractId(self, _contractId):
        return self

    