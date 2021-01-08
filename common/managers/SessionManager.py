from flask import session

KEY_CONTRACT_ID = "contract_id"
KEY_ACCESS_TOKEN = "access_token"


def getByKey(_key):
    if (_key in session):
        return session[_key]
    else:
        return None


def set(_key, value):
    session[_key] = value