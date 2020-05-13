from random import randint

from flask import json

from limbook_api.db import db, BaseDbModel


def create_image(image=None, user_id=None):
    """Generates new image with random attributes for testing
    """
    if image:
        image = Image(**image)
    else:
        rand_user_id = 'auth0|' + str(randint(1000, 9999))
        image = Image(**{
            'user_id': user_id if user_id else rand_user_id,
            'url': json.dumps({
                "thumb": "thumb-" + str(randint(1000, 9999)) + '.jpg',
                "medium": "medium-" + str(randint(1000, 9999)) + '.jpg',
                "large": "large-" + str(randint(1000, 9999)) + '.jpg'
            })
        })

    image.insert()
    return image


class Image(BaseDbModel):
    """Images"""

    id = db.Column(db.Integer, primary_key=True)
    # owner id
    user_id = db.Column(db.String, nullable=False)
    # list of full path of image set (thumbnail, medium, large, full)
    url = db.Column(db.String, nullable=False)

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
