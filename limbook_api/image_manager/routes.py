from flask import Blueprint, jsonify, abort, request

from limbook_api.auth import requires_auth, auth_user_id
from limbook_api.image_manager import Image

images = Blueprint('images', __name__)


def validate_image_data(data):
    # check if image attributes are present
    if not data.get('content'):
        abort(422)


def get_all_images_in_json(post_id):
    # get images
    images = Image.query.filter(Image.post_id == post_id).all()
    # get count
    images_count = Image.query.filter(Image.post_id == post_id).count()

    # format
    data = []
    for image in images:
        data.append(image.format())

    # return the result
    return jsonify({
        'success': True,
        'images': data,
        'images_count': images_count
    })


# ====================================
# ROUTES
# ====================================
@images.route("/posts/<int:post_id>/images", methods=['GET'])
@requires_auth('read:images')
def get_images(post_id):
    """ Get all available images

        Parameters:
             post_id (int): Id of post to which images belong to

        Returns:
            success (boolean)
            images (list)
            total_images (int)
    """
    try:
        return get_all_images_in_json(post_id)
    except Exception as e:
        abort(400)


@images.route("/posts/<int:post_id>/images", methods=['POST'])
@requires_auth('create:images')
def create_images(post_id):
    """ Create new images

        Parameters:
            post_id (int): Id of post to which image will belong

        Internal Parameters:
            content (string): Content for the image
            user_id (string): Internal parameter extracted from current_user

        Returns:
            success (boolean)
            images (list)
            total_images (int)
    """
    # vars
    data = request.get_json()

    validate_image_data(data)

    # create image
    image = Image(**{
        'content': data.get('content'),
        'user_id': auth_user_id(),
        'post_id': post_id
    })

    try:
        image.insert()
        return get_all_images_in_json(post_id)
    except Exception as e:
        abort(400)


@images.route("/posts/<int:post_id>/images/<int:image_id>", methods=['PATCH'])
@requires_auth('update:images')
def update_images(post_id, image_id):
    """ Update images

        Parameters:
            post_id (int): Id of post to which image belong
            image_id (int): Id of image

        Internal Parameters:
            content (string): Content for the image
            user_id (string): Internal parameter extracted from current_user

        Returns:
            success (boolean)
            images (list)
            total_images (int)
    """
    # vars
    data = request.get_json()

    validate_image_data(data)

    # get image
    image = Image.query.first_or_404(image_id)

    # can update own image only
    if image.user_id != auth_user_id():
        abort(403)

    # update image
    image.content = data.get('content')

    try:
        image.update()
        return get_all_images_in_json(post_id)
    except Exception as e:
        abort(400)


@images.route("/posts/<int:post_id>/images/<int:image_id>", methods=['DELETE'])
@requires_auth('delete:images')
def delete_images(post_id, image_id):
    """ Delete images

        Parameters:
            post_id (int): Id of post on which image was made
            image_id (int): Id of image

        Internal Parameters:
            user_id (string): Internal parameter extracted from current_user

        Returns:
            success (boolean)
            images: (list)
            deleted_image (dict)
    """
    # vars
    image = Image.query.first_or_404(image_id)

    # can delete own image only
    if image.user_id != auth_user_id():
        abort(403)

    try:
        image.delete()
        return jsonify({
            "success": True,
            "deleted_image": image.format()
        })
    except Exception as e:
        abort(400)