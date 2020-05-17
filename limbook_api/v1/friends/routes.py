from flask import Blueprint, jsonify, abort, request
from sqlalchemy import or_

from limbook_api.v1.auth.utils import requires_auth, auth_user_id
from limbook_api.v1.friends import Friend, filter_friends

friends = Blueprint('friends', __name__)


# ====================================
# ROUTES
# ====================================
@friends.route("/friends", methods=['GET'])
@requires_auth('read:friends')
def get_friends():
    """ Get all available friends

        Returns:
            success (boolean)
            friends (list)
            total (int)
            query_args (dict)
    """
    try:
        return jsonify({
            'success': True,
            'friends': [
                friend.format() for friend in filter_friends()
            ],
            'total': filter_friends(count_only=True),
            'query_args': request.args,
        })

    except Exception as e:
        abort(400)


@friends.route("/friend-requests", methods=['GET'])
@requires_auth('read:friends')
def get_friend_requests():
    """ Get all friend requests

        Returns:
            success (boolean)
            friend-requests (list)
            total (int)
            query_args (dict)
    """
    try:
        return jsonify({
            'success': True,
            'friend-requests': [
                friend.format() for friend in filter_friends(request_only=True)
            ],
            'total': filter_friends(request_only=True, count_only=True),
            'query_args': request.args,
        })

    except Exception as e:
        abort(400)


@friends.route("/friend-requests", methods=['POST'])
@requires_auth('create:friends')
def create_friend_requests():
    """ Send friend request

        Post data:
            user_id (string): Id of user to send friend request

        Returns:
            success (boolean)
            friend-request (dict)
    """
    data = request.get_json()
    receiver_id = data.get('user_id')

    # See if friend request already exists
    friend = Friend.query.filter(
        or_(
            Friend.requester_id == auth_user_id(),
            Friend.receiver_id == auth_user_id()
        )
    ).filter(Friend.is_friend == False).first()

    if friend is None:
        friend = Friend(**{
            "requester_id": auth_user_id(),
            "receiver_id": receiver_id,
            "is_friend": False
        })
    else:
        abort(400)

    try:
        friend.insert()

        return jsonify({
            "success": True,
            "friend-request": friend.format()
        })

    except Exception as e:
        abort(400)


@friends.route("/friend-requests/<int:friend_request_id>", methods=['PATCH'])
@requires_auth('update:friends')
def update_friend_requests(friend_request_id):
    """ Update friends

        Parameters:
            friend_request_id (string): Friend Id

        Returns:
            success (boolean)
            friend-request (dict)
    """

    friend = Friend.query.first_or_404(friend_request_id)

    if friend.receiver_id != auth_user_id():
        abort(401)

    # See update is_friend to True
    # Only is_friend field is updatable and always to true
    # It means the friend-request has been accepted.
    friend.is_friend = True

    try:
        friend.update()

        return jsonify({
            "success": True,
            "friend-request": friend.format()
        })

    except Exception as e:
        abort(400)


@friends.route("/friends/<int:friend_id>", methods=['DELETE'])
@requires_auth('delete:friends')
def delete_friends(friend_id):
    """ Delete friends

        Delete friends and delete friend-requests are same. These two
        methods exists for user's convenience.

        Parameters:
            friend_id (string): Friend Id

        Returns:
            success (boolean)
            deleted_id (string)
    """

    friend = Friend.query.first_or_404(friend_id)

    # only friend requester or acceptor can terminate friendship
    if friend.requester_id != auth_user_id() \
            and friend.receiver_id != auth_user_id():
        abort(401)

    try:
        friend.delete()

        return jsonify({
            "success": True,
            "deleted_id": friend.id
        })

    except Exception as e:
        abort(400)


@friends.route("/friend-requests/<int:friend_request_id>", methods=['DELETE'])
@requires_auth('delete:friends')
def delete_friend_requests(friend_request_id):
    """ Delete friend request

        Delete friends and delete friend-requests are same. These two
        methods exists for user's convenience.

        Parameters:
            friend_request_id (string): Friend Id

        Returns:
            success (boolean)
            deleted_id (string)
    """

    friend = Friend.query.first_or_404(friend_request_id)

    # only friend requester or acceptor can terminate friendship
    if friend.requester_id != auth_user_id() \
            and friend.receiver_id != auth_user_id():
        abort(401)

    try:
        friend.delete()

        return jsonify({
            "success": True,
            "deleted_id": friend.id
        })

    except Exception as e:
        abort(400)
