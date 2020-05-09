from random import randint

from flask import json
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


def create_random_post():
    """Generates new post with random attributes for testing
    """
    post = Post(**{
        'content': 'Drink ' + str(randint(1000, 9999)),
        'user_id': str(randint(1000, 9999))
    })

    post.insert()
    return post


class Post(db.Model):
    """Posts"""

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    """
    insert()
        inserts a new post into a database
        EXAMPLE
            post = Post(content=req_title, user_id=req_recipe)
            post.insert()
    """
    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
    update()
        updates post in the database
        the model must exist in the database
        EXAMPLE
            post = Post.query.filter(Post.id == id).one_or_none()
            post.content = 'New Content'
            post.update()
    """
    def update(self):
        db.session.commit()

    """
    delete()
        deletes a post from the database
        the model must exist in the database
        EXAMPLE
            post = Post(content=req_title, user_id=req_recipe)
            post.delete()
    """
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())
