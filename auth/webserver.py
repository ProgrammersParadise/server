import cherrypy
from authprovider import AuthProvider
from userprovider import UserProvider
from loginprovider import LoginProvider

def serve(env):
    class Root:
        pass
    
    root = Root()
    root.user = UserProvider(env)
    root.auth = AuthProvider(env)
    root.login = LoginProvider(env)

    def show_blank_page_on_error():
        cherrypy.response.status = 500
        return ''
    
    conf = {
        'global': {
            'server.socket_host': '127.0.0.1',
            'server.socket_port': 14001,
            'request.error_response': show_blank_page_on_error,
        },
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        }
    }
    
    cherrypy.quickstart(root, '/', conf)
