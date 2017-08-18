import cherrypy
import bcrypt

class AuthProvider():
    exposed = True

    def __init__(self, env):
        self.env = env

    def POST(self, name, password):
        cherrypy.response.headers['Content-Type'] = 'text/plain'

        session = self.env.Session()
        res = session.query(self.env.users.c.password).filter(self.env.users.c.name==name).one_or_none()
        if res is None:
            # user not found
            cherrypy.response.status = 401
            return 'FAIL'
        
        oldhash = res.password.encode('utf8')
        newhash = bcrypt.hashpw(password.encode('utf8'), oldhash)

        if newhash != oldhash:
            # passwords don't match
            cherrypy.response.status = 401
            return 'FAIL'

        # everything is okay
        return 'OK'

    def PUT(self, name, password):
        passwordhash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(12))
        statement = self.env.users.insert().values(name=name, password=passwordhash.decode('utf8'))
        self.env.conn.execute(statement)
