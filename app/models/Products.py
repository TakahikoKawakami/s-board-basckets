from tortoise import fields
from app.common.abstracts.AbstractTortoiseModel import AbstractTortoiseModel
from datetime import datetime

class Product(AbstractTortoiseModel):
    """
    商品モデル
    """
    product_id = fields.BigIntField(null=False)
    name = fields.CharField(max_length=255, null=False)
    color = fields.CharField(max_length=64, null=True)
    size = fields.CharField(max_length=64, null=True)
    image = fields.CharField(max_length=511, null=True)
    price = fields.IntField(null=True)
    category_id = fields.IntField(null=True)
    group_code_id = fields.CharField(max_length=255, null=True)


    class Meta:
        abstract=False
        table="products"

    @property
    def productId(self) ->int:
        return self.product_id


    @productId.setter
    def productId(self, val) -> None:
        self.product_id = val
