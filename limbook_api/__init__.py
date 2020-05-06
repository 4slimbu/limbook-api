from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from limbook_api.config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from limbook_api.main.routes import main
    from limbook_api.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app




