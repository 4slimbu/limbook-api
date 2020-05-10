from flask import Blueprint, jsonify, abort, request

from limbook_api.auth.auth import requires_auth
from limbook_api.models.activity import Activity

activities = Blueprint('activities', __name__)


def validate_activity_data(data):
    # check if activity attributes are present
    if not data.get('content'):
        abort(422)


def get_all_activities_in_json(post_id):
    # get activities
    activities = Activity.query.filter(Activity.post_id == post_id).all()
    # get count
    activities_count = Activity.query.filter(Activity.post_id == post_id).count()

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


# ====================================
# ROUTES
# ====================================
@activities.route("/activities", methods=['GET'])
@requires_auth('read:activities')
def get_activities(payload, post_id):
    """ Get all available activities

        Parameters:
             payload (dict): The payload of decoded valid token
             post_id (int): Id of post to which activities belong to

        Returns:
            success (boolean)
            activities (list)
            total_activities (int)
    """
    try:
        return get_all_activities_in_json(post_id)
    except Exception as e:
        abort(400)


@activities.route("/activities", methods=['POST'])
@requires_auth('create:activities')
def create_activities(payload, post_id):
    """ Create new activities

        Parameters:
            payload (dict): The payload of decoded valid token
            post_id (int): Id of post to which activity will belong

        Internal Parameters:
            content (string): Content for the activity
            user_id (string): Internal parameter extracted from current_user

        Returns:
            success (boolean)
            activities (list)
            total_activities (int)
    """
    # vars
    data = request.get_json()

    validate_activity_data(data)

    # create activity
    activity = Activity(**{
        'content': data.get('content'),
        'user_id': payload.get('sub'),
        'post_id': post_id
    })

    try:
        activity.insert()
        return get_all_activities_in_json(post_id)
    except Exception as e:
        abort(400)


@activities.route("/activities/<int:activity_id>", methods=['DELETE'])
@requires_auth('delete:activities')
def delete_activities(payload, post_id, activity_id):
    """ Delete activities

        Parameters:
            payload (dict): The payload of decoded valid token
            post_id (int): Id of post on which activity was made
            activity_id (int): Id of activity

        Internal Parameters:
            user_id (string): Internal parameter extracted from current_user

        Returns:
            success (boolean)
            activities: (list)
            deleted_activity (dict)
    """
    # vars
    activity = Activity.query.first_or_404(activity_id)

    # can delete own activity only
    if activity.user_id != payload.get('sub'):
        abort(403)

    try:
        activity.delete()
        return jsonify({
            "success": True,
            "deleted_activity": activity.format()
        })
    except Exception as e:
        abort(400)