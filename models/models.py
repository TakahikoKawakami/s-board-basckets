from database import db
from sqlalchemy import Column, Integer, Unicode, UnicodeText, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime



class Book(db.Model):
    """
    書籍モデル
    """
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255))
    auther = Column(Unicode(255))
    publisher = Column(Unicode(255))

    #初期化
    def __init__(title, auther, publisher):
        self.title = title.title()
        self.auther = auther.title()
        self.publisher = publisher.title()

class Diary(db.Model):
    """
    感想モデル
    """
    __tablename__ = "diaries"
    id = Column(Integer, primary_key=True)
    date = Column(Unicode(255))
    book_title = Column(Unicode(255), ForeignKey('books.title'))
    impression = Column(UnicodeText)

    #書籍とのリレーションを作成
    book = relationship("Book", backref=backref('diaries', order_by=id))

    #初期化
    def __init__(book_title, impression):
        self.date = datetime.utcnow().strftime( '%Y-%m-%d %H:%M:%S' )
        self.book_title = book_title.title()
        self.impression = impression.title()


