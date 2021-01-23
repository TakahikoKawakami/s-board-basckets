KEY_CONTRACT_ID = "contract_id"
KEY_ACCESS_TOKEN = "access_token"
KEY_ACCESS_TOKEN_EXPIRES_IN = "access_token_expires_in"
KEY_QUERY_PARAMS_FOR_REDIRECT = "query_params_for_redirect"


def has(reqSession, _key):
    try:
        if (_key in reqSession):
            return True
        else:
            return False
    except Exception:
        return False


def get(reqSession, _key):
    try:
        if (_key in reqSession):
            return reqSession[_key]
        else:
            return None
    except Exception:
        return None

def set(respSession, _key, value):
    respSession[_key] = value


def remove(respSession, _key):
    respSession.pop(_key)