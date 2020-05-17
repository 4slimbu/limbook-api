import os


class Config:
    # -------------------------------------------
    # App
    # -------------------------------------------

    # Enable debug mode
    DEBUG = True

    # App secret
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_secret_key')

    # Pagination
    PAGINATION = 10

    # Access token validity in seconds
    ACCESS_TOKEN_VALID_TIME = 10 * 60

    # Refresh token validity in seconds
    REFRESH_TOKEN_VALID_TIME = 60 * 60

    # -------------------------------------------
    # Flask-Caching
    # -------------------------------------------
    CACHE_TYPE = "simple"

    CACHE_DEFAULT_TIMEOUT = 300

    # -------------------------------------------
    # Database
    # -------------------------------------------

    # Database uri
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:password@localhost:5432/limbook_api"

    # Display or Hide sqlalchemy track modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -------------------------------------------
    # Image
    # -------------------------------------------

    # Limit the max allowed payload to 2mb
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024

    # Allowed extensions
    ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg'}

    # Sizes to generate while saving image
    IMG_SIZES = {
        "thumb": (150, 150),
        "medium": (768, 768),
        "large": (1080, 1080)
    }

    # Image upload directory
    IMG_UPLOAD_DIR = 'limbook_api/static/img/uploads'

    # -------------------------------------------
    # Email
    # -------------------------------------------
    EMAIL_DRIVER = 'flask-mail'

    # -------------------------------------------
    # Authentication
    # -------------------------------------------
    AUTH_DRIVER = 'auth0'
    AUTH0_DOMAIN = 'limvus.auth0.com'
    ALGORITHMS = ['RS256']
    API_AUDIENCE = 'limbook-auth-api'
