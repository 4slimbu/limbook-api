from flask import Blueprint, jsonify, abort, request, json

from limbook_api.v1.auth.utils import requires_auth, auth_user_id
from limbook_api.v1.image_manager import Image, create_img_set, \
    validate_image_data, filter_images
from limbook_api.v1.posts import Post, get_images_list_using_ids

image_manager = Blueprint('image_manager', __name__)


# ====================================
# ROUTES
# ====================================
@image_manager.route("/images", methods=['GET'])
@requires_auth('read:images')
def get_images():
    """ Update images

        Query params:
            page (int)
            post_id (int)

        Returns:
            success (boolean)
            images (list): List of images
            total (int)
            query_args (dict)
    """

    try:
        return jsonify({
            'success': True,
            'images': [
                image.format() for image in filter_images()
            ],
            'total': filter_images(count_only=True),
            'query_args': request.args,
        })
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
            delete_id (int)
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
            "deleted_id": image.id
        })
    except Exception as e:
        abort(400)


@image_manager.route("/posts/<int:post_id>/images", methods=['POST'])
@requires_auth('update:posts')
def attach_images_to_post(post_id):
    """ Attach images to post

        Parameters:
            post_id (int): Id of post

        Post data:
            image_ids (list): List of image ids

        Returns:
            success (boolean)
            post (dict)
    """
    # vars
    post = Post.query.first_or_404(post_id)

    # can attach images to own post only
    if post.user_id != auth_user_id():
        abort(403)

    # attach images
    data = request.get_json()
    image_ids = data.get('image_ids')
    images = get_images_list_using_ids(image_ids)

    try:
        post.images = images
        post.update()
        return jsonify({
            "success": True,
            "post": post.format()
        })
    except Exception as e:
        abort(400)
