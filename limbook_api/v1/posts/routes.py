from flask import Blueprint, jsonify, abort, request

from limbook_api.v1.auth import requires_auth, auth_user_id
from limbook_api.v1.posts import Post, get_all_posts_in_json, validate_post_data

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
            total_posts (int)
    """
    try:
        return get_all_posts_in_json()
    except Exception as e:
        abort(400)


@posts.route("/posts", methods=['POST'])
@requires_auth('create:posts')
def create_posts():
    """ Create new posts

        Internal Parameters:
            content (string): Content for the post
            user_id (string): Internal parameter extracted from current_user

        Returns:
            success (boolean)
            posts (list)
            total_posts (int)
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
        return get_all_posts_in_json()
    except Exception as e:
        abort(400)


@posts.route("/posts/<int:post_id>", methods=['PATCH'])
@requires_auth('update:posts')
def update_posts(post_id):
    """ Update posts

        Parameters:
            post_id (int): Id of post

        Internal Parameters:
            content (string): Content for the post
            user_id (string): Internal parameter extracted from current_user

        Returns:
            success (boolean)
            posts (list)
            total_posts (int)
    """
    # vars
    data = request.get_json()

    validate_post_data(data)

    # get post
    post = Post.query.first_or_404(post_id)

    # can update own post only
    if post.user_id != auth_user_id():
        abort(403)

    # update post
    post.content = data.get('content')

    try:
        post.update()
        return get_all_posts_in_json()
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
            "deleted_post": post.format()
        })
    except Exception as e:
        abort(400)
