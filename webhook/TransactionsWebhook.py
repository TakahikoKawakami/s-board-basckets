from flask import request
from webhook import route


@route.before_request
def beforeRequest():
    pass        
    # transactionsApi.config.accessToken = session['access_token']
    # transactionsApi.config.contractId = session['contract_id']
#    if not ('contract_id' in session):
#        if ()
#    self.getToken()


@route.route('/accounts', methods=['POST'])
def signUp():
    print('signUp!!!')
    return '', 200

@route.route('', methods=['POST'])
def webhook():
    print(request.get_data())
    return '', 200