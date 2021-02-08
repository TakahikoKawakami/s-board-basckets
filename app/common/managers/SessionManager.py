KEY_ACCOUNT = "account"
KEY_ACCOUNT_SETTING = "account"
KEY_CONTRACT_ID = "contract_id"
KEY_ACCESS_TOKEN = "access_token"
KEY_ACCESS_TOKEN_EXPIRATION_DATETIME = "access_token_expiration_datetime"
KEY_TARGET_STORE = "target_store_id"
KEY_QUERY_PARAMS_FOR_REDIRECT = "query_params_for_redirect"
KEY_ERROR_MESSAGES = "error_message_for_redirect"
KEY_CSRF_TOKEN = "csrf_token"
KEY_SIGN_UP = "sign_up"


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
    try:
        if (_key in respSession):
            respSession.pop(_key)
    except Exception:
        pass