from core.settings.base import Config


class TestingConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgres://username:password@host:port/test_database"
