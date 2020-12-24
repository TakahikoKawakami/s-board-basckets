import os
import sys
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from application import app
from database import db


migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='0.0.0.0', port='5500'))



#app.pyをターミナルから直接呼び出した時だけ、app.run()を実行する
if __name__ == "__main__":
    args = sys.argv
    if ('db' in args) or ('runserver' in args):
        manager.run()
        db.create_all()
    else: # 引数がない場合(debug用)
        # app.run(debug=True, use_reloader=False, host='0.0.0.0' ,port=5500)
        app.run(debug=True, use_reloader=True, host='0.0.0.0' ,port=5500)
