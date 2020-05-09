import os


class Config:
    # Enable debug mode
    DEBUG = True

    # App secret
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = "my_secret_key"
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:password@localhost:5432/limbook_api"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
