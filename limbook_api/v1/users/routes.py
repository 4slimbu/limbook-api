from flask import Blueprint, jsonify, abort, request

from limbook_api.v1.auth.utils import requires_auth, auth_user_id
from limbook_api.v1.users import User, filter_users, \
    validate_user_data, validate_user_update_data

users = Blueprint('users', __name__)


# ====================================
# ROUTES
# ====================================
@users.route("/users", methods=['GET'])
@requires_auth('read:users')
def get_users():
    """ Get all available users

        Query Parameters:
             search_term (str)
             page (int)

        Returns:
            success (boolean)
            users (list)
            total (int)
            query_args (dict)
    """
    try:
        return jsonify({
            'success': True,
            'users': [
                user.format() for user in filter_users()
            ],
            'total': filter_users(count_only=True),
            'query_args': request.args,
        })
    except Exception as e:
        abort(400)


@users.route("/users", methods=['POST'])
@requires_auth('create:users')
def create_users():
    """ Create new users

        Post data:
            first_name (string)
            last_name (string)
            email (string)
            phone_number (string)
            password (string)
            confirm_password (string)
            profile_picture (string)
            cover_picture (string)

        Returns:
            success (boolean)
            user (dict)
    """
    # vars
    data = validate_user_data(request.get_json())

    # create user
    user = User(**data)

    try:
        user.insert()

        return jsonify({
            "success": True,
            "user": user.format()
        })
    except Exception as e:
        abort(400)


@users.route("/users/<int:user_id>", methods=['PATCH'])
@requires_auth('update:users')
def update_users(user_id):
    """ Update users

        Parameters:
            user_id (int): Id of user

        Patch data:
            first_name (string)
            last_name (string)
            email (string)
            phone_number (string)
            password (string)
            confirm_password (string)
            profile_picture (string)
            cover_picture (string)
            role_id (int)

        Returns:
            success (boolean)
            user (dict)
    """
    # vars
    data = validate_user_update_data(request.get_json())

    # get user
    user = User.query.first_or_404(user_id)

    # TODO: implement this
    # can update own user only
    # if user.id != auth_user_id():
    #     abort(403)

    try:
        user.query.update(data)
        return jsonify({
            "success": True,
            "user": user.format()
        })
    except Exception as e:
        abort(400)


@users.route(
    "/users/<int:user_id>", methods=['DELETE'])
@requires_auth('delete:users')
def delete_users(user_id):
    """ Delete users

        Parameters:
            user_id (int): Id of user

        Returns:
            success (boolean)
            deleted_id (int)
    """
    # vars
    user = User.query.first_or_404(user_id)

    # TODO: implement this
    # can delete own user only
    # if user.id != auth_user_id():
    #     abort(403)

    try:
        user.delete()
        return jsonify({
            "success": True,
            "deleted_id": user.id
        })
    except Exception as e:
        abort(400)
