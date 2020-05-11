from flask import json

from limbook_api.setup_db import db


class Image(db.Model):
    """Images"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    post_id = db.Column(
        db.Integer,
        db.ForeignKey('post.id', ondelete="cascade"),
        nullable=False
    )
    post = db.relationship('Post', backref=db.backref(
        'images', lazy=True, cascade="all, delete"))
    """
    insert()
        inserts a new image into a database
        EXAMPLE
            image = Image(content=req_title, post_id=req_recipe)
            image.insert()
    """
    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
    update()
        updates image in the database
        the model must exist in the database
        EXAMPLE
            image = Image.query.filter(Image.id == id).one_or_none()
            image.content = 'New Content'
            image.update()
    """
    def update(self):
        db.session.commit()

    """
    delete()
        deletes a image from the database
        the model must exist in the database
        EXAMPLE
            image = Image(content=req_title, post_id=req_recipe)
            image.delete()
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
            'name': self.name,
            'post_id': self.post_id,
        }

    def __repr__(self):
        return json.dumps(self.format())
