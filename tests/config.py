import os


class Config:
    # Enable debug mode
    DEBUG = True

    # App secret
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = 'my_secret_test_key'

    # Configure SQLAlchemy and database
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site_test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

