from sqlalchemy import Column, Integer, Unicode, UnicodeText, ForeignKey, Boolean, Date, DateTime, Enum, Text
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from pprint import pprint
from datetime import datetime
import json
import app.database as db

import logging

class AbstractModel(db.Base):
    """
    アブストラクトモデル
    """
    __abstract__ = True 
    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Unicode(32), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    modified_at = Column(DateTime, default=datetime.now())

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

