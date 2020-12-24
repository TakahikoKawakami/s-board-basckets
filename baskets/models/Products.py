from sqlalchemy import Column, Integer, Unicode, UnicodeText, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship, backref
from datetime import datetime

from database import db


class Product(db.Model):
    """
    商品モデル
    """
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Unicode(32), nullable=False)
    name = Column(Unicode(255), nullable=False)
    color = Column(Unicode(64), nullable=False)
    size = Column(Unicode(64))
    image = Column(Unicode(511))
    price = Column(Integer)
    category_id = Column(Integer)
    group_code_id = Column(Unicode(255))

    created_at = Column(DateTime)
    modified_at = Column(DateTime)

    #初期化
    def __init__(self):
        pass


    def __repr__(self):
        return "Product<{}, {}, {}>".format(self.id, self.productId, self.productName)


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
