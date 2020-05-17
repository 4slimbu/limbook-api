from flask import json

from limbook_api.db import db, BaseDbModel


class Activity(BaseDbModel):
    """Activities"""

    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    action = db.Column(
        db.Enum(
            'commented', 'reacted', 'created', 'updated', 'deleted',
            name="actions"
        ),
        nullable=False
    )

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
            'created_on': self.created_on.__str__(),
            'updated_on': self.updated_on.__str__(),
        }

    def __repr__(self):
        return json.dumps(self.format())
