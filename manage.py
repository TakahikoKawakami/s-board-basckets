import os
import sys
from flask import Flask,\
                  render_template,\
                  request,\
                  redirect,\
                  url_for,\
                  session,\
                  Blueprint

# sys.path.append(os.getcwd()) # 現在のディレクトリを環境変数に一時的に取り込む

from authorizations.controllers import AuthController
from baskets.controllers import BasketController
from application import Application
from database import Database



homeRoute =  Blueprint('home', __name__)
@homeRoute.route('/')
def index():
    from authorizations.models import Accounts
    account = Accounts.Account
    accounts = account.query.order_by(account.id.asc())
    return render_template("books/index.html",
                            accounts=accounts,
                            message = '')


routes = [
    AuthController.route,
    BasketController.route,
    homeRoute
]

app = Application()
app.setRoute(routes)



#app.pyをターミナルから直接呼び出した時だけ、app.run()を実行する
if __name__ == "__main__":
    args = sys.argv
    if ('db' in args) or ('runserver' in args):
        app.manager.run()
        app.db.create_all()
    else: # 引数がない場合(debug用)
        app.app.run(debug=True, use_reloader=False)
