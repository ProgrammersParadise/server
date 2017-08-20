import cherrypy
import datetime
import json

class LoginProvider:
    exposed = True

    def __init__(self, env):
        self.env = env

    def POST(self, token):
        session = self.env.Session()
        now = datetime.datetime.utcnow()
        res = session.query(self.env.tokens.c.userid).filter(self.env.tokens.c.expires>now, self.env.tokens.c.token==token).one_or_none()
        if res is None:
            # user not found
            cherrypy.response.status = 401
            cherrypy.response.headers['Content-Type'] = 'text/plain'
            return 'FAIL'
        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps({'userid': int(res.userid)}).encode('utf8')
