from core.settings.base import Config


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Homosapiens_81@localhost:5432/findaz"
