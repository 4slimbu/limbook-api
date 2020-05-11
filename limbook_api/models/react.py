from flask import json
from random import randint

from limbook_api.models import db


def create_react(react=None):
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
