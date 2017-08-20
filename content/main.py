#!/usr/bin/env python2

import cherrypy
import requests

class Root:
    pass

class LoginProvider:
    exposed = True

    def POST(self, username, password):
        r = requests.post('http://127.0.0.1:14001/auth', data={'username': username, 'password': password});
        cherrypy.response.headers['Content-Type'] = r.headers['content-type']
        return r.text

class ProtectedResource:
    """
    Returns a tuple. First argument is true on successful validation
    while the second tuple element is the userid. On failure the first
    tuple element is False and the second a reason.
    """
    def validate_token(self):
        if not 'Authorization' in cherrypy.request.headers:
            return (False, 'This resource is protected and needs an authorization token')
        auth = cherrypy.request.headers['Authorization'];
        (authType, token,) = auth.split(' ');
        if authType != 'Token':
            return (False, 'This operation requires a valid access token')
        # ask the auth backend if the token is valid
        r = requests.post('http://127.0.0.1:14001/login', data={'token': token});
        if r.status_code != 200:
            return (False, 'The token is invalid: {0}'.format(r.text))
        return (True, r.json()['userid'])

class IdeaProvider:
    exposed = True

    pass

class CategoryProvider(ProtectedResource):
    exposed = True

    def GET(self):
        (login_valid, login_result) = self.validate_token()
        if login_valid != True:
            cherrypy.response.status = 401
            return login_result
        return 'Success! Sadly this is not implemented yet, but your internal userid is {0}'.format(login_result)


root = Root()
root.login = LoginProvider()
root.category = CategoryProvider()
root.idea = IdeaProvider()

def show_blank_page_on_error():
    cherrypy.response.status = 500
    return ''

conf = {
    'global': {
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 14002,
        'request.error_response': show_blank_page_on_error,
    },
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
    }
}

cherrypy.quickstart(root, '/', conf)
