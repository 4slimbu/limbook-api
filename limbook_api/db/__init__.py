from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate(compare_type=True)
flask_seeder = FlaskSeeder()

from limbook_api.db.base_model import BaseDbModel  # noqa: E402


def setup_db(app):
    """ Binds a flask application and a SQLAlchemy service"""
    db.app = app
    db.init_app(app)

    # setup migration
    migrate.init_app(app, db)

    # setup flask seed
    flask_seeder.init_app(app, db)


def db_drop_and_create_all():
    """Drops the database tables and start fresh"""
    db.drop_all()
    db.create_all()
