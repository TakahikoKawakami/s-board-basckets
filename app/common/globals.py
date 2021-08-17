from app.models import Account


class Global():
    __login_account = Account()

    def login(self, account: Account) -> Account:
        global __login_account
        self.__login_account = account
        return self.__login_account

    @property
    def logged_in_account(self) -> Account:
        return self.__login_account


globals = Global()
