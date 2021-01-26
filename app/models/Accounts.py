from tortoise import fields
from datetime import datetime

from app.common.abstracts.AbstractTortoiseModel import AbstractTortoiseModel
from app.entities.AccessToken import AccessToken


class Account(AbstractTortoiseModel):
    """
    アカウントモデル
    """
    STATUS_START = 'start'
    STATUS_STOP = 'stop'

    access_token = fields.CharField(max_length=1024)
    expiration_date_time = fields.DatetimeField()
    status = fields.CharField(max_length=16)

    class Meta:
        abstract=False
        table="accounts"

    @property
    def contractId(self):
        return self.contract_id

    @contractId.setter
    def contractId(self, contractId):
        self.contract_id = contractId

    @property
    def accessToken(self):
        accessToken = AccessToken(self.access_token, self.expiration_date_time)
        return accessToken

    @accessToken.setter
    def accessToken(self, accessToken):
        self.access_token = accessToken.accessToken
        self.expiration_date_time = accessToken.expirationDatetime

    @property
    def expirationDatetime(self):
        return self.expiration_date_time

    @classmethod
    def create(cls, contractId, accessToken):
        return super().create(
            contract_id = contractId,
            access_token = accessToken.accessToken,
            expiration_date_time = accessToken.expirationDatetime,
            status = cls.STATUS_START
        )
