import os

class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60
    TESTING = False
    DEBUG = False


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///shop.db"
    DEBUG = True


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
    TESTING = True
    DEBUG = True

    # Disable rate limiting while testing
    RATELIMIT_ENABLED = False

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URI") or 'sqlite:///app.db'
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = False
    TESTING = False
