from flask import json

from limbook_api.db import db, BaseDbModel

post_image = db.Table(
    'post_image',
    db.Column(
        'post_id', db.Integer,
        db.ForeignKey('post.id', ondelete="cascade"),
        primary_key=True
    ),
    db.Column(
        'image_id', db.Integer,
        db.ForeignKey('image.id'),
        primary_key=True
    )
)


class Image(BaseDbModel):
    """Images"""

    id = db.Column(db.Integer, primary_key=True)
    # owner id
    user_id = db.Column(db.String, nullable=False)
    # list of full path of image set (thumbnail, medium, large, full)
    url = db.Column(db.String, nullable=False)

    post = db.relationship(
        'Post', secondary=post_image,
        backref=db.backref('images', lazy=True)
    )

    """
    delete()
        deletes a image from the database
        the model must exist in the database
    """
    def delete(self):
        # delete image file
        from limbook_api.image_manager import delete_image_set
        delete_image_set(self)
        # delete image data
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
            'url': json.loads(self.url),
            'created_on': self.created_on.__str__(),
            'updated_on': self.updated_on.__str__()
        }
