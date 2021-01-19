from sqlalchemy import Column, Integer, Unicode, UnicodeText, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship, backref
from datetime import datetime

import app.database as db
from app.common.abstracts.AbstractModel import AbstractModel


class Product(AbstractModel):
    """
    商品モデル
    """
    __tablename__ = "products"
    product_id = Column(Integer)
    name = Column(Unicode(255), nullable=False)
    color = Column(Unicode(64))
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
        return "Product<{}, {}>".format(self.product_id, self.productName)


    @property
    def productId(self) ->int:
        return self.product_id


    @productId.setter
    def productId(self, val) -> None:
        self.product_id = val