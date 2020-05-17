from limbook_api.db import db, BaseDbModel


class React(BaseDbModel):
    """Reacts"""

    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(
        db.Integer, db.ForeignKey('post.id'),
        nullable=False
    )
    post = db.relationship(
        'Post', backref='reacts', uselist=False,
        lazy=True
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
        }
