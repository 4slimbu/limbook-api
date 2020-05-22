from flask import Blueprint, jsonify, abort, request
from sqlalchemy import or_

from limbook_api.v1.auth.utils import requires_auth, auth_user_id
from limbook_api.v1.friends import Friend, filter_friends
from limbook_api.v1.posts import filter_posts
from limbook_api.v1.users import User

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
        user_ids = [
            (
                friend.requester_id if friend.requester_id != auth_user_id()
                else friend.receiver_id
            ) for friend in filter_friends()
        ]

        users = User.query.filter(User.id.in_(user_ids)).all()

        friends = []
        for friend in users:
            friends.append({
                "id": friend.id,
                "first_name": friend.first_name,
                "last_name": friend.last_name,
                "profile_picture": friend.profile_picture
            })

        return jsonify({
            'success': True,
            'friends': friends,
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


@friends.route("/send-friend-request", methods=['POST'])
@requires_auth('create:friends')
def send_friend_requests():
    """ Send friend request

        Post data:
            user_id (string): Id of user to send friend request

        Returns:
            success (boolean)
            friend-request (dict)
    """
    try:
        data = request.get_json()
        receiver_id = data.get('user_id')

        # See if friend request already exists
        friend_request_sent = Friend.query.filter(
            Friend.requester_id == auth_user_id(),
            Friend.receiver_id == receiver_id,
            Friend.is_friend == 1
        ).first()

        friend_request_received = Friend.query.filter(
            Friend.requester_id == receiver_id,
            Friend.receiver_id == auth_user_id(),
            Friend.is_friend == 1
        ).first()

        if friend_request_sent is None and friend_request_received is None:
            pass
        else:
            abort(400)

        friend = Friend(**{
            "requester_id": auth_user_id(),
            "receiver_id": receiver_id,
            "is_friend": False
        })

        friend.insert()

        return jsonify({
            "success": True,
            "friend-request": friend.format()
        })

    except Exception as e:
        abort(400)


@friends.route("/accept-friend-request", methods=['POST'])
@requires_auth('create:friends')
def accept_friend_requests():
    """ Accept friend request

        Post data:
            friend_request_id (string): Id of friend request

        Returns:
            success (boolean)
            friend-request (dict)
    """
    data = request.get_json()
    friend_request_id = data.get('friend_request_id')

    friend = Friend.query.filter(Friend.id == friend_request_id).first_or_404()

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

    friend = Friend.query.filter(Friend.id == friend_id).first_or_404()

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

    friend = Friend.query.filter(Friend.id == friend_request_id).first_or_404()

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
