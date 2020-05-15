from os import abort
from random import randint

from flask import jsonify

from limbook_api.v1.activities import Activity


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
        'user_id': user_id if user_id else str(randint(1000, 9999)),
        'action': action if action else a_enum[randint(0, len(a_enum) - 1)],
        'post_id': post_id if post_id else str(randint(1000, 9999))
    })

    activity.insert()
    return activity


def validate_activity_data(data):
    # check if activity attributes are present
    if not data.get('content'):
        abort(422)


def get_all_activities_in_json(user_id):
    # get activities
    activities = Activity.query.filter(Activity.user_id == user_id).all()
    # get count
    activities_count = Activity.query.filter(Activity.user_id == user_id).count()

    # format
    data = []
    for activity in activities:
        data.append(activity.format())

    # return the result
    return jsonify({
        'success': True,
        'activities': data,
        'activities_count': activities_count
    })