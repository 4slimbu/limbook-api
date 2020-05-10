from flask import Blueprint, jsonify, abort

from limbook_api.auth.auth import requires_auth, auth_user_id
from limbook_api.models.activity import Activity

activities = Blueprint('activities', __name__)


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


# ====================================
# ROUTES
# ====================================
@activities.route("/activities", methods=['GET'])
@requires_auth('read:activities')
def get_activities():
    """ Get all available activities

        Returns:
            success (boolean)
            activities (list)
            total_activities (int)
    """
    try:
        user_id = auth_user_id()
        return get_all_activities_in_json(user_id)
    except Exception as e:
        abort(400)


@activities.route("/activities/<int:activity_id>", methods=['DELETE'])
@requires_auth('delete:activities')
def delete_activities(activity_id):
    """ Delete activities

        Parameters:
            activity_id (int): Id of activity

        Returns:
            success (boolean)
            activities: (list)
            deleted_activity (dict)
    """
    # vars
    activity = Activity.query.first_or_404(activity_id)

    # can delete own activity only
    if activity.user_id != auth_user_id():
        abort(403)

    try:
        activity.delete()
        return jsonify({
            "success": True,
            "deleted_activity": activity.format()
        })
    except Exception as e:
        abort(400)
