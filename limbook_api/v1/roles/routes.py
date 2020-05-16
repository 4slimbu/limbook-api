from flask import Blueprint, jsonify, abort, request

from limbook_api.v1.auth import requires_auth, auth_user_id
from limbook_api.v1.roles import Role, filter_roles, \
    validate_role_data, validate_role_update_data

roles = Blueprint('roles', __name__)


# ====================================
# ROUTES
# ====================================
@roles.route("/roles", methods=['GET'])
@requires_auth('read:roles')
def get_roles():
    """ Get all available roles

        Query Parameters:
             search_term (str)
             page (int)

        Returns:
            success (boolean)
            roles (list)
            total (int)
            query_args (dict)
    """
    try:
        return jsonify({
            'success': True,
            'roles': [
                role.format() for role in filter_roles()
            ],
            'total': filter_roles(count_only=True),
            'query_args': request.args,
        })
    except Exception as e:
        abort(400)


@roles.route("/roles", methods=['POST'])
@requires_auth('create:roles')
def create_roles():
    """ Create new roles

        Post data:
            slug (string)
            name (string)
            description (string)

        Returns:
            success (boolean)
            role (dict)
    """
    # vars
    data = validate_role_data(request.get_json())

    try:
        # create role
        role = Role(**data)
        role.insert()

        return jsonify({
            "success": True,
            "role": role.format()
        })
    except Exception as e:
        abort(400)


@roles.route("/roles/<int:role_id>", methods=['PATCH'])
@requires_auth('update:roles')
def update_roles(role_id):
    """ Update roles

        Parameters:
            role_id (int): Id of role

        Patch data:
            name (string)
            description (string)

        Returns:
            success (boolean)
            role (dict)
    """
    # vars
    data = validate_role_update_data(request.get_json())

    # get role
    role = Role.query.first_or_404(role_id)

    # TODO: implement this
    # can update own role only
    # if role.id != auth_role_id():
    #     abort(403)

    try:
        role.query.update(data)
        return jsonify({
            "success": True,
            "role": role.format()
        })
    except Exception as e:
        abort(400)


@roles.route(
    "/roles/<int:role_id>", methods=['DELETE'])
@requires_auth('delete:roles')
def delete_roles(role_id):
    """ Delete roles

        Parameters:
            role_id (int): Id of role

        Returns:
            success (boolean)
            deleted_id (int)
    """
    # vars
    role = Role.query.first_or_404(role_id)

    # TODO: implement this
    # can delete own role only
    # if role.id != auth_role_id():
    #     abort(403)

    try:
        role.delete()
        return jsonify({
            "success": True,
            "deleted_id": role.id
        })
    except Exception as e:
        abort(400)
