import os
import cherrypy
import bcrypt
import datetime
import sqlalchemy
import json

class AuthProvider():
    exposed = True

    def __init__(self, env):
        self.max_sessions_per_user = 5
        self.env = env

    def POST(self, username, password):
        session = self.env.Session()
        res = session.query(self.env.users.c.id, self.env.users.c.password).filter(self.env.users.c.username==username).one_or_none()
        if res is None:
            # user not found
            cherrypy.response.status = 401
            cherrypy.response.headers['Content-Type'] = 'text/plain'
            return 'FAIL'

        userid = res.id
        oldhash = res.password.encode('utf8')
        newhash = bcrypt.hashpw(password.encode('utf8'), oldhash)

        if newhash != oldhash:
            # passwords don't match
            cherrypy.response.status = 401
            cherrypy.response.headers['Content-Type'] = 'text/plain'
            return 'FAIL'

        # everything is okay, create token
        insertCompleted = False
        expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        while not insertCompleted:
            token = ''.join('%02x' % ord(chr(x)) for x in os.urandom(32))
            statement = self.env.tokens.insert().values(token=token,
                                                        expires=expires,
                                                        userid=userid)
            self.env.conn.execute(statement)
            insertCompleted = True

        # allow at most N sessions per user id
        lastSession = session.query(self.env.tokens.c.id).filter(self.env.tokens.c.userid==userid).order_by(self.env.tokens.c.id.desc()).offset(self.max_sessions_per_user).limit(1).one_or_none()
        # if we found more than N, then delete those
        if not lastSession is None:
            statement = self.env.tokens.delete().where(sqlalchemy.and_(self.env.tokens.c.userid==userid, self.env.tokens.c.id <= lastSession))
            self.env.conn.execute(statement)

        cherrypy.response.headers['Content-Type'] = 'application/json'
        return json.dumps({
            'token': token,
            'expires': str(expires)
        }).encode('utf8')
