from sqlalchemy import Column, Integer, Unicode, UnicodeText, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship, backref
from datetime import datetime

from database import Database


class Account(Database.db.Model):
    """
    アカウントモデル
    """
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Unicode(32), nullable=False)
    status = Column(Unicode(32))
    created_at = Column(DateTime)
    modified_at = Column(DateTime)

    #初期化
    def __init__(self, contractId, status):
        self.contract_id = contractId
        self.status = status

    def __repr__(self):
        return "Account<{}, {}, {}>".format(self.id, self.contract_id, self.status)

    def register(self):
        # insert into users(name, address, tel, mail) values(...)
        Database.db.session.add(self)
        Database.db.session.commit()
        return self
    
    def delete(self):
        Database.db.session.delete(self)
        Database.db.session.commit()
        return self

def showByContractId(_contractId):
    account = Database.db.session.query(Account).filter(Account.contract_id == _contractId).first()
    return account
#    return Account(account.contract_id, account.status)


if __name__ == "__main__":
    pass
