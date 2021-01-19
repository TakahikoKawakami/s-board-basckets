from sqlalchemy import Column, Integer, Unicode, UnicodeText, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship, backref
from datetime import datetime

from app.common.abstracts.AbstractModel import AbstractModel
import app.database as db


class Account(AbstractModel):
    """
    アカウントモデル
    """
    STATUS_START = 'start'
    STATUS_STOP = 'stop'
    
    __tablename__ = "accounts"
    contract_id = Column(Unicode(32), nullable=False)
    access_token = Column(Unicode(128), nullable=True)
    expiration_date_time = Column(DateTime, nullable=True)
    status = Column(Unicode(32))

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
    def expirationDateTime(self):
        return self.expiration_date_time

    @expirationDateTime.setter
    def expirationDateTime(self, expirationDateTime):
        self.expiration_date_time = expirationDateTime

    def register(self):
        # insert into users(name, address, tel, mail) values(...)
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

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

    