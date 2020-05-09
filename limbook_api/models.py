from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def setup_db(app):
    """ Binds a flask application and a SQLAlchemy service"""
    db.app = app
    db.init_app(app)

    # setup migration
    Migrate(app, db)

    # setup flask seed
    FlaskSeeder(app, db)


def db_drop_and_create_all():
    """Drops the database tables and start fresh"""
    db.drop_all()
    db.create_all()
