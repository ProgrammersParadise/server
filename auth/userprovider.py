import os
import cherrypy
import bcrypt

class UserProvider():
    exposed = True

    def __init__(self, env):
        self.env = env

    def PUT(self, username, password):
        passwordhash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(12))
        statement = self.env.users.insert().values(username=username, password=passwordhash.decode('utf8'))
        self.env.conn.execute(statement)
        return 'OK'
