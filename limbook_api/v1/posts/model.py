from limbook_api.db import db, BaseDbModel


class Post(BaseDbModel):
    """Posts"""

    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False)

    """
    format()
        format the data for the api
    """
    def format(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'images': [image.format() for image in self.images],
            'reacts': [react.format() for react in self.reacts],
            'comments': [comment.format() for comment in self.comments]
        }
