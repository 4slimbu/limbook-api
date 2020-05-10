from flask import Blueprint, jsonify, abort, request

from limbook_api.auth.auth import requires_auth, auth_user_id
from limbook_api.models.react import React

reacts = Blueprint('reacts', __name__)


def validate_react_data(data):
    # check if react attributes are present
    if not data.get('content'):
        abort(422)


def get_all_reacts_in_json(post_id, user_id):
    # get reacts
    reacts = React.query.filter(
        React.post_id == post_id,
        React.user_id == user_id
    ).all()

    # get count
    reacts_count = React.query.filter(
        React.post_id == post_id,
        React.user_id == user_id
    ).count()

    # format
    data = []
    for react in reacts:
        data.append(react.format())

    # return the result
    return jsonify({
        'success': True,
        'reacts': data,
        'reacts_count': reacts_count
    })


# ====================================
# ROUTES
# ====================================
@reacts.route("/posts/<int:post_id>/reacts", methods=['GET'])
@requires_auth('read:reacts')
def get_reacts(post_id):
    """ Get all available reacts

        Parameters:
             post_id (int): Id of post to which reacts belong to

        Returns:
            success (boolean)
            reacts (list)
            total_reacts (int)
    """
    try:
        return get_all_reacts_in_json(post_id)
    except Exception as e:
        abort(400)


@reacts.route("/posts/<int:post_id>/reacts/toggle", methods=['POST'])
# TODO: fix caps on Create:reacts and use it
@requires_auth('update:reacts')
def create_reacts(post_id):
    """ Create new react or delete if exist

        Parameters:
            post_id (int): Id of post to which react will belong

        Internal Parameters:
            user_id (string): Internal parameter extracted from current_user

        Returns:
            success (boolean)
            reacts (list)
            total_reacts (int)
    """
    try:
        user_id = auth_user_id()
        user_react = React.query.filter(
            React.post_id == post_id,
            React.user_id == auth_user_id()
        ).one_or_none()

        # toggle react
        if user_react is None:
            # create react
            react = React(**{
                'user_id': auth_user_id(),
                'post_id': post_id
            })

            react.insert()
        else:
            # delete
            user_react.delete()

        return get_all_reacts_in_json(post_id, user_id)

    except Exception as e:
        abort(400)
