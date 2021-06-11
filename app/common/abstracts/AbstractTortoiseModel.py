from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class AbstractTortoiseModel(Model):
    """
    アブストラクトモデル
    """
    contract_id = fields.CharField(max_length=32)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True

    async def serialize(self):
        selfPydantic = pydantic_model_creator(self.__class__)
        p = await selfPydantic.from_tortoise_orm(self)
        return p.json(indent=4)
