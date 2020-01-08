class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = b'\_5#y2L"F4Q8z\n\xec]/'
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
