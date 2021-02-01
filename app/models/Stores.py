from tortoise import fields
from app.common.abstracts.AbstractTortoiseModel import AbstractTortoiseModel
from datetime import datetime

class Store(AbstractTortoiseModel):
    """
    店舗t品モデル
    """
    store_id = fields.IntField(null=False)
    name = fields.CharField(max_length=255, null=False)


    class Meta:
        abstract=False
        table="stores"

    @property
    def storeId(self) ->int:
        return self.store_id


    @storeId.setter
    def storeId(self, val) -> None:
        self.store_id = val