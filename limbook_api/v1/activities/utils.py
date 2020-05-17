from os import abort
from random import randint

from flask import request

from limbook_api.db.utils import filter_model
from limbook_api.v1.activities import Activity
from limbook_api.v1.auth.utils import auth_user_id


def generate_activity(user_id=None, action=None, post_id=None):
    """Create new activity

        Parameter:
            user_id (string) : Auth0 id
            action (string) : e.g: 'commented', 'reacted' etc.
            post_id (int) : Post id
        Returns:
            Activity (Model)
    """
    a_enum = ['commented', 'reacted', 'created', 'updated', 'deleted']
    activity = Activity(**{
        'user_id': user_id if user_id else randint(1000, 9999),
        'action': action if action else a_enum[randint(0, len(a_enum) - 1)],
        'post_id': post_id if post_id else randint(1000, 9999)
    })

    activity.insert()
    return activity


def validate_activity_data(data):
    # check if activity attributes are present
    if not data.get('action'):
        abort(422)


def filter_activities(count_only=False):
    query = Activity.query

    # add search filter
    if request.args.get('search_term'):
        query = query.filter(Activity.action.ilike(
                "%{}%".format(request.args.get('search_term'))
            ))

    # activity belongs to user
    query = query.filter(Activity.user_id == auth_user_id())

    # return filtered data
    return filter_model(Activity, query, count_only=count_only)
