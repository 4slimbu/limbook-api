from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from limbook_api.config import Config
from limbook_api.db import setup_db
from limbook_api.errors import AuthError, ImageUploadError
from limbook_api.errors.error_handlers import register_error_handlers

db = SQLAlchemy()


def create_app(config_class=Config):
    """ Creates the flask app"""

    # instantiate and configure flask app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # setup database related extensions
    setup_db(app)

    # register blueprints
    from limbook_api.main.routes import main
    from limbook_api.posts.routes import posts
    from limbook_api.reacts.routes import reacts
    from limbook_api.comments.routes import comments
    from limbook_api.activities.routes import activities
    from limbook_api.image_manager.routes import image_manager
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(reacts)
    app.register_blueprint(comments)
    app.register_blueprint(activities)
    app.register_blueprint(image_manager)

    # register error handlers
    register_error_handlers(app)

    # return flask app
    return app
