import sqlalchemy
from sqlalchemy.orm import sessionmaker
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class Env:
    def __init__(self):
        dbcfg = config['database']
        uri = (
            dbcfg['type']
            + '://' + dbcfg['username']
            + ':'   + dbcfg['password']
            + '@'   + dbcfg['host']
            + '/'   + dbcfg['database']
        )
        self.engine = sqlalchemy.create_engine(uri, isolation_level='AUTOCOMMIT');
        self.conn = self.engine.connect()
        self.Session = sessionmaker(bind=self.engine)

        self.metadata = sqlalchemy.MetaData()
        self.users = sqlalchemy.Table('users', self.metadata,
                                      sqlalchemy.Column('id', sqlalchemy.Integer,
                                                        sqlalchemy.Sequence('id_seq'),
                                                        primary_key=True),
                                      sqlalchemy.Column('name', sqlalchemy.Text,
                                                        unique=True,
                                                        index=True),
                                      sqlalchemy.Column('password', sqlalchemy.Text))
        self.metadata.bind = self.engine
        self.metadata.create_all(checkfirst=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

