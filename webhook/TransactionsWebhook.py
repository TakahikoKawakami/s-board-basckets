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
def webhook():
    print('webhook!!!')
    return '', 200