from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_mail import Mail
from rq import Queue

from config import Config
from limbook_api.db import setup_db
from limbook_api.errors import AuthError, ImageUploadError
from limbook_api.errors.error_handlers import register_error_handlers
from limbook_api.v1 import register_v1_blueprints
from worker import conn

bcrypt = Bcrypt()
cache = Cache()
mail = Mail()
q = Queue(connection=conn)

def create_app(config_class=Config):
    """ Creates the flask app"""

    # instantiate and configure flask app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # setup database related extensions
    setup_db(app)

    # setup flask caching
    cache.init_app(app)

    # setup bcrypt
    bcrypt.init_app(app)

    # setup flask mail
    mail.init_app(app)

    # register blueprints
    register_v1_blueprints(app)

    # register error handlers
    register_error_handlers(app)

    @app.route("/")
    def home():
        return render_template('home.html')

    # return flask app
    return app
