import sys
from flask import Flask, render_template, request, redirect, url_for, session
from database import db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

import settings

import models as models

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False


#デバッグ
app.config['DEBUG'] = True
#秘密キー
app.secret_key = settings.SECRET_KEY
#データベースを指定
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URI
app.config['SQLALCHEMY_NATIVE_UNICODE'] = 'utf-8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
db.app = app

migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='localhost', port='8080'))


@app.route('/')
def index():
    account = models.accounts.Account
    accounts = account.query.order_by(account.id.asc())
    return render_template("books/index.html",
                            accounts=accounts)
                            
@app.route('/test', methods=['GET', 'POST'])
def test():
    try:
        if request.method == 'GET': # login
            if ('contract_id' in session):
                account = models.accounts.showByContractId(session['contract_id'])
                if (account != None):
                    return 'logined ' + account.contract_id
                else:
                    session.pop['contract_id']
                    return 'session failed ?'
            else:
                _contractId = request.args.get('contract_id', '')
                account = models.accounts.showByContractId(_contractId)
                if (account != None):
                    session['contract_id'] = _contractId
                    return 'set'
                else:
                    return 'who?'
        elif request.method == 'POST':
            _contractId = request.form['contract_id']
            _status = request.form['status']
            account = models.accounts.Account(_contractId, _status).all()
            registeredAccount = account.register()
            return redirect('/')
        else:
            return abort(400)
    except Exception as e:
        return str(e)

@app.route('/test/delete', methods=['POST'])
def testDelete():
    try:
        if request.method == 'POST':
            contractId = request.form['contract_id']
            account = models.accounts.showByContractId(contractId)
            if (account == None):
                return 'non type error'
            account.delete()
            return redirect('/')
        else:
            return abort(400)
    except Exception as e:
        return str(e)

#app.pyをターミナルから直接呼び出した時だけ、app.run()を実行する
if __name__ == "__main__":
    args = sys.argv
    if ('db' in args) or ('runserver' in args):
        manager.run()
        db.create_all()
    else: # 引数がない場合(debug用)
        app.run(debug=True, use_reloader=False)
