from flask import json

from limbook_api.db import db


class BaseDbModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, default=db.func.now())
    updated_on = db.Column(
        db.DateTime, default=db.func.now(),
        onupdate=db.func.now()
    )
    """
    insert()
        inserts a new image into a database
    """

    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
    update()
        updates image in the database
        the model must exist in the database
    """

    def update(self):
        db.session.commit()

    """
    delete()
        deletes a image from the database
        the model must exist in the database
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
            'id': self.id
        }

    def __repr__(self):
        return json.dumps(self.format())
