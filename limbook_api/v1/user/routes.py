from flask import Blueprint, request, jsonify, abort

from limbook_api.v1.auth.utils import requires_auth, \
    auth_user_id, validate_profile_data
from limbook_api.v1.posts import Post

personal = Blueprint('user', __name__)


@personal.route("/profile", methods=['GET'])
@requires_auth()
def get_profile():
    """ Get auth user info

    Returns:
        success (boolean)
        user (dict)
    """
    user = User.query.filter(User.id == auth_user_id()).first_or_404()
    return jsonify({
        "success": True,
        "user": user.format()
    })


@personal.route("/profile", methods=['PATCH'])
@requires_auth()
def update_profile():
    """ Update profile

    Patch data:
        first_name (string)
        last_name (string)
        phone_number (string)
        password (string)
        confirm_password (string)
        profile_picture (string)
        cover_picture (string)

    Returns:
        success (boolean)
        user (dict)
    """
    data = validate_profile_data(request.get_json())

    # get user
    user = User.query.filter(User.id == auth_user_id()).first_or_404()

    try:
        user.query.update(data)
        user.update()
        return jsonify({
            "success": True,
            "user": user.format()
        })
    except Exception as e:
        abort(400)


@personal.route("/timeline", methods=['GET'])
@requires_auth()
def timeline():
    """ Get all posts by auth user

    Returns:
        success (boolean)
        posts (list)
        total (int)
        query_args (dic)
    """
    try:
        query = Post.query.filter(Post.user_id == auth_user_id())
        posts = filter_model(Post, query, count_only=False)
        total = filter_model(Post, query, count_only=True)
        return jsonify({
            'success': True,
            'posts': [
                post.format() for post in posts
            ],
            'total': total,
            'query_args': request.args,
        })
    except Exception as e:
        abort(400)


@personal.route("/news-feed", methods=['GET'])
@requires_auth()
def news_feed():
    """ Get all posts by auth user and friends

        Returns:
            success (boolean)
            posts (list)
            total (int)
            query_args (dic)
        """
    try:
        user_ids = [
            (
                friend.requester_id if friend.requester_id != auth_user_id()
                else friend.receiver_id
            ) for friend in filter_friends()
        ]
        user_ids.append(auth_user_id())

        query = Post.query.filter(Post.user_id.in_(user_ids))
        posts = filter_model(Post, query, count_only=False)
        total = filter_model(Post, query, count_only=True)
        return jsonify({
            'success': True,
            'posts': [
                post.format() for post in posts
            ],
            'total': total,
            'query_args': request.args,
        })
    except Exception as e:
        abort(400)
