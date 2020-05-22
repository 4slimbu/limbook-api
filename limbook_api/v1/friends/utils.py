from random import randint

from sqlalchemy import or_

from limbook_api.db.utils import filter_model
from limbook_api.v1.auth.utils import auth_user_id
from limbook_api.v1.friends import Friend


def generate_friend_request(requester_id=None, receiver_id=None):
    return generate_friend(requester_id, receiver_id, is_friend=False)


def generate_friend(requester_id=None, receiver_id=None, is_friend=True):
    """Generates new friend with random attributes for testing
    """
    friend = Friend(**{
        'requester_id': requester_id if requester_id else randint(1000, 9999),
        'receiver_id': receiver_id if receiver_id else randint(1000, 9999),
        'is_friend': is_friend
    })

    friend.insert()
    return friend


def filter_friends(request_only=False, count_only=False):
    query = Friend.query

    # is friends
    if request_only:
        # filter requests only
        query = query.filter(Friend.is_friend == bool(False))

        # request received by current user
        query = query.filter(
            Friend.receiver_id == auth_user_id()
        )

    else:
        # filter friends only
        query = query.filter(Friend.is_friend == bool(True))

        # get friends
        query = query.filter(
            or_(
                Friend.requester_id == auth_user_id(),
                Friend.receiver_id == auth_user_id()
            )
        )

    # return filtered data
    return filter_model(Friend, query, count_only=count_only)
