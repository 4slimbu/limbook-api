import os


class Config:
    # -------------------------------------------
    # App
    # -------------------------------------------

    # App url
    APP_URL = 'http://localhost:5000'

    # Enable debug mode
    DEBUG = True

    # App secret
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Pagination
    PAGINATION = 10

    # Access token validity in seconds
    ACCESS_TOKEN_VALID_TIME = 10 * 60

    # Refresh token validity in seconds
    REFRESH_TOKEN_VALID_TIME = 60 * 60

    # Initial roles and permissions
    #
    # It may not reflect the current roles and permissions in the system
    # as user with ability to manage roles and permissions can change as
    # per the need of the system. But it is useful for setting up the
    # database for the first time. The permissions are used throughout
    # the system, so before updating permissions make sure permissions in
    # the affected routes are updated as well.
    #
    # manage:all -> can manage everything
    # manage:item -> can manage everything related to item
    # manage_self:item -> can manage own item
    INITIAL_ROLES_AND_PERMISSIONS = {
        "admin": [
            'read:users', 'create:users', 'update:users', 'delete:users',
            'read:roles', 'create:roles', 'update:roles', 'delete:roles',
            'read:permissions', 'create:permissions', 'update:permissions',
            'delete:permissions',
            'read:posts', 'create:posts', 'update:posts', 'delete:posts',
            'read:comments', 'create:comments', 'update:comments',
            'delete:comments',
            'read:reacts', 'create:reacts', 'update:reacts', 'delete:reacts',
            'read:images', 'create:images', 'update:images', 'delete:images',
            'read:friends', 'create:friends', 'update:friends', 'delete:friends'
        ],
        "user": [
            'read:posts', 'create:posts', 'update:posts', 'delete:posts',
            'read:comments', 'create:comments', 'update:comments',
            'delete:comments',
            'read:reacts', 'create:reacts', 'update:reacts', 'delete:reacts',
            'read:images', 'create:images', 'update:images', 'delete:images',
            'read:friends', 'create:friends', 'update:friends', 'delete:friends'
        ],
        "unverified_user": []
    }

    # -------------------------------------------
    # Flask-Caching
    # -------------------------------------------
    CACHE_TYPE = "simple"

    CACHE_DEFAULT_TIMEOUT = 300

    # -------------------------------------------
    # Database
    # -------------------------------------------

    # Database uri
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    # Display or Hide sqlalchemy track modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -------------------------------------------
    # Redis
    # -------------------------------------------
    USE_REDIS = True
    REDIS_URL = os.environ.get('REDIS_URL')

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
    IMG_UPLOAD_DIR = '/static/img/uploads'

    # -------------------------------------------
    # Email
    # -------------------------------------------
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
