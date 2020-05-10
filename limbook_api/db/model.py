from random import randint

from flask import json
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()
migrate = Migrate(compare_type=True)
flask_seeder = FlaskSeeder()


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


def create_random_post(post=None):
    """Generates new post with random attributes for testing
    """
    if post:
        post = Post(**post)
    else:
        post = Post(**{
            'content': 'Post ' + str(randint(1000, 9999)),
            'user_id': str(randint(1000, 9999))
        })

    post.insert()
    return post


class Post(db.Model):
    """Posts"""

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False)

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

    """
    format()
        format the data for the api
    """
    def format(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
        }

    def __repr__(self):
        return json.dumps(self.format())


def create_random_comment(comment=None):
    """Generates new comment with random attributes for testing
    """
    if comment:
        comment = Comment(**comment)
    else:
        comment = Comment(**{
            'content': 'Comment ' + str(randint(1000, 9999)),
            'user_id': str(randint(1000, 9999)),
            'post_id': str(randint(1000, 9999)),
        })

    comment.insert()
    return comment


class Comment(db.Model):
    """Comments"""

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=True)

    """
    insert()
        inserts a new comment into a database
        EXAMPLE
            comment = Comment(content="new comment", user_id="auth0|id", post_id=1)
            comment.insert()
    """
    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
    update()
        updates comment in the database
        the model must exist in the database
        EXAMPLE
            comment = Comment.query.filter(Comment.id == id).one_or_none()
            comment.content = 'New Content'
            comment.update()
    """
    def update(self):
        db.session.commit()

    """
    delete()
        deletes a comment from the database
        the model must exist in the database
        EXAMPLE
            comment = Comment.query.filter(Comment.id == id).one_or_none()
            comment.delete()
    """
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    """
    format()
        format the data for the api
    """
    def format(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'created_at': self.created_at.__str__(),
            'updated_at': self.updated_at.__str__(),
        }

    def __repr__(self):
        return json.dumps(self.format())


def create_random_react(react=None):
    """Generates new react with random attributes for testing
    """
    if react:
        react = React(**react)
    else:
        react = React(**{
            'user_id': str(randint(1000, 9999)),
            'post_id': str(randint(1000, 9999)),
        })

    react.insert()
    return react


class React(db.Model):
    """Reacts"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)

    """
    insert()
        inserts a new react into a database
        EXAMPLE
            react = React(user_id="auth0|id", post_id=1)
            react.insert()
    """
    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
    delete()
        deletes a react from the database
        the model must exist in the database
        EXAMPLE
            react = React.query.filter(React.id == id).one_or_none()
            react.delete()
    """
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    """
    format()
        format the data for the api
    """
    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
        }

    def __repr__(self):
        return json.dumps(self.format())
