from flask import Blueprint, jsonify, abort, request

from limbook_api.v1.auth.utils import requires_auth, auth_user_id
from limbook_api.v1.activities import Activity, filter_activities

activities = Blueprint('activities', __name__)


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
            total (int)
            query_args (dict)
    """
    try:
        return jsonify({
            'success': True,
            'activities': [
                activity.format() for activity in filter_activities()
            ],
            'total': filter_activities(count_only=True),
            'query_args': request.args,
        })
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
            "deleted_id": activity.id
        })
    except Exception as e:
        abort(400)
