import os

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format( os.path.join(os.path.dirname(__file__), 'bookingdb.db'))
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format( os.path.join(os.path.dirname(__file__), 'bookingdb.db'))
    SQLALCHEMY_ECHO = False
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format( os.path.join(os.path.dirname(__file__), 'bookingdb.db'))
    SQLALCHEMY_ECHO = False