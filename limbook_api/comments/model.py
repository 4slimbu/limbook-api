from limbook_api.db import db, BaseDbModel


class Comment(BaseDbModel):
    """Comments"""

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False)
    post_id = db.Column(
        db.Integer, db.ForeignKey('post.id'),
        nullable=False
    )
    post = db.relationship(
        'Post', backref='comments', uselist=False,
        lazy=True
    )

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
            'created_on': self.created_on.__str__(),
            'updated_on': self.updated_on.__str__(),
        }
