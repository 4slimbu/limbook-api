class Config:
    # Enable debug mode
    DEBUG = True

    # App secret
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = "my_secret_key"
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:password@localhost:5432/limbook_api"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Limit the max allowed payload to 2mb
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024

    # Allowed extensions
    ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg'}

    # Imag sizes
    IMG_SIZES = {
        "thumb": (150, 150),
        "medium": (768, 768),
        "large": (1080, 1080)
    }
    # Image upload path relative to app root directory
    IMG_UPLOAD_DIR = 'static/img/uploads'

    # Auth0 credentials
    AUTH0_DOMAIN = 'limvus.auth0.com'
    ALGORITHMS = ['RS256']
    API_AUDIENCE = 'limbook-auth-api'
