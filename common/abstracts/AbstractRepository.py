from datetime import datetime

import common.managers.SessionManager as sessionManager
from database import db

class AbstractRepository():
    def __init__(self):
        pass


    @staticmethod
    def commit():
        db.session.commit()
        

    @staticmethod
    def rollback():
        db.session.rollback()
    