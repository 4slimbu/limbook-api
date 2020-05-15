from random import randint

from flask import jsonify
from sqlalchemy import or_

from limbook_api.v1.auth import auth_user_id
from limbook_api.v1.friends import Friend


def generate_friend(requester_id=None, receiver_id=None, is_friend=None):
    """Generates new friend with random attributes for testing
    """
    friend = Friend(**{
        'requester_id': requester_id if requester_id else str(randint(1000, 9999)),
        'receiver_id': receiver_id if receiver_id else str(randint(1000, 9999)),
        'is_friend': is_friend if is_friend else False
    })

    friend.insert()
    return friend


def get_all_friends_in_json():
    # get friends
    friends = Friend.query.filter(
        or_(
            Friend.requester_id == auth_user_id(),
            Friend.receiver_id == auth_user_id()
        )
    ).all()

    # get count
    friends_count = Friend.query.filter(
        or_(
            Friend.requester_id == auth_user_id(),
            Friend.receiver_id == auth_user_id()
        )
    ).count()

    # format
    data = []
    for friend in friends:
        data.append(friend.format())

    # return the result
    return jsonify({
        'success': True,
        'friends': data,
        'friends_count': friends_count
    })
