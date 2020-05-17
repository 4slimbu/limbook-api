from flask import Blueprint, jsonify, abort, request

from limbook_api.v1.auth.utils import requires_auth, auth_user_id
from limbook_api.v1.posts import Post, validate_post_data, filter_posts, \
    get_images_list_using_ids

posts = Blueprint('posts', __name__)


# ====================================
# ROUTES
# ====================================
@posts.route("/posts", methods=['GET'])
@requires_auth('read:posts')
def get_posts():
    """ Get all available posts

        Returns:
            success (boolean)
            posts (list)
            total (int)
            query_args (dic)
    """
    try:
        return jsonify({
            'success': True,
            'posts': [
                post.format() for post in filter_posts()
            ],
            'total': filter_posts(count_only=True),
            'query_args': request.args,
        })
    except Exception as e:
        abort(400)


@posts.route("/posts", methods=['POST'])
@requires_auth('create:posts')
def create_posts():
    """ Create new posts

        Post data:
            content (string): Content for the post
            image_ids (list|optional): Ids of uploaded images

        Returns:
            success (boolean)
            post (list)
    """
    # vars
    data = request.get_json()

    validate_post_data(data)

    # create post
    post = Post(**{
        'content': data.get('content'),
        'user_id': auth_user_id()
    })

    try:
        post.insert()

        # attach images
        image_ids = data.get('image_ids')
        if image_ids:
            images = get_images_list_using_ids(image_ids)
            post.images = images
            post.update()

        return jsonify({
            "success": True,
            "post": post.format()
        })
    except Exception as e:
        abort(400)


@posts.route("/posts/<int:post_id>", methods=['PATCH'])
@requires_auth('update:posts')
def update_posts(post_id):
    """ Update posts

        Parameters:
            post_id (int): Id of post

        Patch data:
            content (string|optional): Content for the post
            image_ids (list|optional):
                Internal parameter extracted from current_user

        Returns:
            success (boolean)
            posts (list)
            total_posts (int)
    """
    # vars
    data = request.get_json()

    # get post
    post = Post.query.first_or_404(post_id)

    # can update own post only
    if post.user_id != auth_user_id():
        abort(403)

    try:
        # update post
        content = data.get('content')
        if content:
            post.content = data.get('content')
            post.update()

        # update images
        image_ids = data.get('image_ids')
        if image_ids:
            # delete images
            for image in post.images:
                image.delete()

            # attach images
            images = get_images_list_using_ids(image_ids)
            post.images = images
            post.update()

        return jsonify({
            "success": True,
            "post": post.format()
        })
    except Exception as e:
        abort(400)


@posts.route("/posts/<int:post_id>", methods=['DELETE'])
@requires_auth('delete:posts')
def delete_posts(post_id):
    """ Delete posts

        Parameters:
            post_id (int): Id of post

        Internal Parameters:
            user_id (string): Internal parameter extracted from current_user

        Returns:
            success (boolean)
            deleted_post (dict)
    """
    # vars
    post = Post.query.first_or_404(post_id)

    # can delete own post only
    if post.user_id != auth_user_id():
        abort(403)

    try:
        # delete images
        for image in post.images:
            image.delete()

        # delete post
        post.delete()

        return jsonify({
            "success": True,
            "deleted_id": post.id
        })
    except Exception as e:
        abort(400)
