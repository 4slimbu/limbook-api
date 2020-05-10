from flask import Blueprint, jsonify, abort, request

from limbook_api.auth.auth import requires_auth
from limbook_api.db.main import Post

posts = Blueprint('posts', __name__)


def validate_post_data(data):
    # check if post attributes are present
    if not data.get('content'):
        abort(422)


def get_all_posts_in_json():
    # get posts
    posts = Post.query.all()
    # get count
    posts_count = Post.query.count()

    # format
    data = []
    for post in posts:
        data.append(post.format())

    # return the result
    return jsonify({
        'success': True,
        'posts': data,
        'posts_count': posts_count
    })


# ====================================
# ROUTES
# ====================================
@posts.route("/posts", methods=['GET'])
@requires_auth('read:posts')
def get_posts(payload):
    """ Get all available posts

        Parameters (dict): The payload of decoded valid token

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
def create_posts(payload):
    """ Create new posts

        Parameters:
            payload (dict): The payload of decoded valid token

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
        'user_id': payload.get('sub')
    })

    try:
        post.insert()
        return get_all_posts_in_json()
    except Exception as e:
        abort(400)


@posts.route("/posts/<int:post_id>", methods=['PATCH'])
@requires_auth('update:posts')
def update_posts(payload, post_id):
    """ Update posts

        Parameters:
            payload (dict): The payload of decoded valid token
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
    if post.user_id != payload.get('sub'):
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
def delete_posts(payload, post_id):
    """ Delete posts

        Parameters:
            payload (dict): The payload of decoded valid token
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
    if post.user_id != payload.get('sub'):
        abort(403)

    try:
        post.delete()
        return jsonify({
            "success": True,
            "deleted_post": post.format()
        })
    except Exception as e:
        abort(400)