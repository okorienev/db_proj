class Config(object):
    debug = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://test:test@postgres/db1'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_POOL_TIMEOUT = 5
    admin_login = 'admin'
    admin_pass = 'admin'
    pass
