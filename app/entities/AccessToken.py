from smaregipy.entities.account import Account


class AccessToken(Account.AccessToken):
    def __init__(self, _access_token, _expiration_datetime):
        super().__init__(_access_token, _expiration_datetime)
