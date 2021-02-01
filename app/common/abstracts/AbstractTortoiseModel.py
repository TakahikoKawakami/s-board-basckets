from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from datetime import datetime
from pprint import pprint
from datetime import datetime
import json
import app.database as db

import logging

class AbstractTortoiseModel(Model):
    """
    アブストラクトモデル
    """
    contract_id = fields.CharField(max_length=32)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


    def __repr__(self):
        pass

    @property
    async def serialize(self):
        selfPydantic = pydantic_model_creator(self.__class__)
        p = await selfPydantic.from_tortoise_orm(self)
        return p.json(indent=4)

    @property
    def contractId(self):
        return self.contract_id


    @contractId.setter
    def contractId(self, val):
        self.contract_id = val


    @property
    def modifiedAt(self):
        return self.modified_at

    
    @modifiedAt.setter
    def modifiedAt(self, val):
        self.modified_at = val


    @property
    def createdAt(self):
        return self.created_at

    
    @createdAt.setter
    def createdAt(self, val):
        self.created_at = val


    def register(self):
        # insert into users(name, address, tel, mail) values(..)
        db.session.add(self)
        db.session.flush()
        return self
    

    def delete(self):
        db.session.delete(self)
        db.session.flush()
        return self

