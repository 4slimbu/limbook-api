from flask import json
from random import randint

from limbook_api.models.setup import db


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
