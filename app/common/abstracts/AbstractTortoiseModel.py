from tortoise.models import Model
from tortoise import fields

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
    __abstract__ = True 
    id = fields.IntField(pk=True)
    contract_id = fields.CharField(max_length=32)
    created_at = fields.DatetimeField(default=datetime.now())
    modified_at = fields.DatetimeField(default=datetime.now())

    #初期化
    def __init__(self):
        pass


    def __repr__(self):
        pass


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

