from sqlalchemy import Column, Integer, Unicode, UnicodeText, ForeignKey, Boolean, DateTime, Enum, Text
from sqlalchemy.orm import relationship, backref
from datetime import datetime

from database import db


class Transactions(db.Model):
    """
    取引モデル
    """
    __tablename__ = "transactions"
    contract_id = Column(Unicode(32), nullable=False)
    transaction_id = Column(Integer, nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    transaction_date_division = Column(Integer, nullable=False) # 2時間区切り
    basket = Column(Text, nullable=False) # 商品IDのカンマ区切り
    member_id = Column(Integer, nullable=False)
    customer_group_id = Column(Integer, nullable=False)
    store_id = Column()
    created_at = Column(DateTime)
    modified_at = Column(DateTime)

    #初期化
    def __init__(self):
        pass


    def __repr__(self):
        return "Transactions<{}, {}, {}>".format(self.id, self.transactionId, self.transactionDate)


    def register(self):
        # insert into users(name, address, tel, mail) values(...)
        db.session.add(self)
        db.session.commit()
        return self
    

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self


    def showByProductId(self, _contractId, _productId):
        product = db.session.query(self).filter(
            self.contract_id == _contractId,
            self.id == _productId
        ).first()
        return account
