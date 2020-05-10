from flask import json
from random import randint
from sqlalchemy import func

from limbook_api.models.setup import db


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