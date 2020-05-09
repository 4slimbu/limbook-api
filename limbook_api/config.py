import os


class Config:
    # Enable debug mode
    DEBUG = True

    # App secret
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = 'my_secret_key'

    # Configure SQLAlchemy and database
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # Auth0 credentials
    AUTH0_DOMAIN = 'limvus.auth0.com'
    ALGORITHMS = ['RS256']
    API_AUDIENCE = 'coffee-shop-auth'
