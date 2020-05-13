from flask import Blueprint, jsonify, abort, request, json

from limbook_api.auth import requires_auth, auth_user_id
from limbook_api.image_manager import Image, create_img_set, delete_image_set

image_manager = Blueprint('image_manager', __name__)


def validate_image_data(data):
    # check if image attributes are present
    if not data.get('image'):
        abort(422)


def get_all_user_images_in_json():
    # get images
    images = Image.query.filter(Image.user_id == auth_user_id()).all()
    # get count
    images_count = Image.query.filter(Image.user_id == auth_user_id()).count()

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
@image_manager.route("/images", methods=['GET'])
@requires_auth('read:images')
def get_images():
    """ Update images

        Returns:
            success (boolean)
            images (list): List of images
            images_count (int)
    """

    try:
        # return the result
        return get_all_user_images_in_json()
    except Exception as e:
        abort(400)


@image_manager.route("/images/<int:image_id>", methods=['GET'])
@requires_auth('read:images')
def get_image(image_id):
    """ Update images

        Parameters:
            image_id (int): Id of image

        Returns:
            success (boolean)
            image (dist)
    """
    # get image
    image = Image.query.first_or_404(image_id)

    # can retrieve own image only
    if image.user_id != auth_user_id():
        abort(403)

    try:
        # return the result
        return jsonify({
            'success': True,
            'image': image.format()
        })
    except Exception as e:
        abort(400)


@image_manager.route("/images", methods=['POST'])
@requires_auth('create:images')
def create_images():
    """ Create new images

        Internal Parameters:
            image (FileStorage): Image

        Returns:
            success (boolean)
            image (list)
    """
    # vars
    image_file = request.files.get('image')

    validate_image_data({"image": image_file})

    image_url_set = create_img_set(image_file)

    # create image
    image = Image(**{
        "user_id": auth_user_id(),
        "url": json.dumps(image_url_set)
    })

    try:
        image.insert()
        # return the result
        return jsonify({
            'success': True,
            'image': image.format()
        })
    except Exception as e:
        abort(400)


@image_manager.route("/images/<int:image_id>", methods=['DELETE'])
@requires_auth('delete:images')
def delete_images(image_id):
    """ Delete images

        Parameters:
            image_id (int): Id of image

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
        deleted_image = image.format()
        delete_image_set(deleted_image.get('url'))
        return jsonify({
            "success": True,
            "deleted_image": deleted_image
        })
    except Exception as e:
        abort(400)
