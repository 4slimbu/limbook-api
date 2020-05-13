from flask import json
from random import randint
from sqlalchemy import func

from limbook_api.db import db


def create_activity(activity=None):
    """Create new activity

        Parameter:
            activity (dict | optional): If present use this else generate dummy
                {
                    "user_id": "auth0|id",
                    "action": "commented",
                    "post_id": 1
                }

        Returns:
            Activity (Model)
    """
    if activity:
        activity = Activity(**activity)
    else:
        action = ['commented', 'reacted', 'created', 'updated', 'deleted']
        activity = Activity(**{
            'user_id': str(randint(1000, 9999)),
            'action': action[randint(0, len(action) - 1)],
            'post_id': str(randint(1000, 9999)),
        })

    activity.insert()
    return activity


class Activity(db.Model):
    """Activities"""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    action = db.Column(
        db.Enum('commented', 'reacted', 'created', 'updated', 'deleted', name="actions"),
        nullable=False
    )
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime, nullable=True)

    """
    insert()
        inserts a new activity into a database
        EXAMPLE
            activity = Activity(user_id="auth0|id", action="created", post_id=1)
            activity.insert()
    """
    def insert(self):
        db.session.add(self)
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
            'user_id': self.user_id,
            'post_id': self.post_id,
            'action': self.action,
            'created_at': self.created_at.__str__(),
            'updated_at': self.updated_at.__str__(),
        }

    def __repr__(self):
        return json.dumps(self.format())