from limbook_api.db import db, BaseDbModel


class Friend(BaseDbModel):
    """Friends"""

    requester_id = db.Column(db.Integer, nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    is_friend = db.Column(db.Boolean, nullable=False, default=False)

    """
    format()
        format the data for the api
    """
    def format(self):
        return {
            'id': self.id,
            'requester_id': self.requester_id,
            'receiver_id': self.receiver_id,
            'is_friend': self.is_friend
        }
