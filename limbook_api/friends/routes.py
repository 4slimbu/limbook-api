from flask import Blueprint, jsonify, abort, request

from limbook_api.auth import requires_auth, auth_user_id
from limbook_api.friends import Friend
from limbook_api.friends import get_all_friends_in_json

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
            total_friends (int)
    """
    try:
        return get_all_friends_in_json()
    except Exception as e:
        abort(400)


@friends.route("/friends", methods=['POST'])
@requires_auth('create:friends')
def create_friends():
    """ Create new friends

        Internal Parameters:
            user_id (string): Internal parameter extracted from current_user

        Returns:
            success (boolean)
    """
    data = request.get_json()
    receiver_id = data.get('user_id')

    # See if friend request already exists
    friend = Friend.query.filter(
        Friend.receiver_id == receiver_id,
        Friend.is_friend == False
    ).first()

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
            "friend": friend.format()
        })

    except Exception as e:
        abort(400)


@friends.route("/friends/<friend_id>", methods=['PATCH'])
@requires_auth('update:friends')
def update_friends(friend_id):
    """ Update friends

        Parameters:
            friend_id (string): Friend Id

        Returns:
            success (boolean)
            friend (dict)
    """

    friend = Friend.query.first_or_404(friend_id)

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
            "friend": friend.format()
        })

    except Exception as e:
        abort(400)


@friends.route("/friends/<friend_id>", methods=['DELETE'])
@requires_auth('delete:friends')
def delete_friends(friend_id):
    """ Delete friends

        Parameters:
            friend_id (string): Friend Id

        Returns:
            success (boolean)
            friend (dict)
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

