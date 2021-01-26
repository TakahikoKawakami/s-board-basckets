import responder

def bookRedirect(resp):
    return resp.headers.get('Location') is not None