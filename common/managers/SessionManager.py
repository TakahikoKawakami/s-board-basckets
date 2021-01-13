from flask import session

KEY_CONTRACT_ID = "contract_id"
KEY_ACCESS_TOKEN = "access_token"
KEY_ACCESS_TOKEN_EXPIRES_IN = "access_token_expires_in"
KEY_QUERY_PARAMS_FOR_REDIRECT = "query_params_for_redirect"

def getByKey(_key):
    if (_key in session):
        return session[_key]
    else:
        return None


def get(_key):
    if (_key in session):
        return session[_key]
    else:
        return None


def set(_key, value):
    session[_key] = value


def remove(_key):
    session.pop(_key)