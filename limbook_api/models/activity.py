from flask import json
from random import randint
from sqlalchemy import func

from limbook_api.models.setup import db


def create_random_activity(activity=None):
    """Generates new activity with random attributes for testing
    """
    if activity:
        activity = Activity(**activity)
    else:
        activity = Activity(**{
            'content': 'Activity ' + str(randint(1000, 9999)),
            'user_id': str(randint(1000, 9999)),
            'post_id': str(randint(1000, 9999)),
        })

    activity.insert()
    return activity


class Activity(db.Model):
    """Activities"""

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=True)

    """
    insert()
        inserts a new activity into a database
        EXAMPLE
            activity = Activity(content="new activity", user_id="auth0|id", post_id=1)
            activity.insert()
    """
    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
    update()
        updates activity in the database
        the model must exist in the database
        EXAMPLE
            activity = Activity.query.filter(Activity.id == id).one_or_none()
            activity.content = 'New Content'
            activity.update()
    """
    def update(self):
        db.session.commit()

    """
    delete()
        deletes a activity from the database
        the model must exist in the database
        EXAMPLE
            activity = Activity.query.filter(Activity.id == id).one_or_none()
            activity.delete()
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