from flask import Blueprint, jsonify, abort, request

from limbook_api.v1.auth.utils import requires_auth, auth_user_id
from limbook_api.v1.permissions import Permission, filter_permissions, \
    validate_permission_data, validate_permission_update_data

permissions = Blueprint('permissions', __name__)


# ====================================
# ROUTES
# ====================================
@permissions.route("/permissions", methods=['GET'])
@requires_auth('read:permissions')
def get_permissions():
    """ Get all available permissions

        Query Parameters:
             search_term (str)
             page (int)

        Returns:
            success (boolean)
            permissions (list)
            total (int)
            query_args (dict)
    """
    try:
        return jsonify({
            'success': True,
            'permissions': [
                permission.format() for permission in filter_permissions()
            ],
            'total': filter_permissions(count_only=True),
            'query_args': request.args,
        })
    except Exception as e:
        abort(400)


@permissions.route("/permissions", methods=['POST'])
@requires_auth('create:permissions')
def create_permissions():
    """ Create new permissions

        Post data:
            slug (string)
            name (string)
            description (string)

        Returns:
            success (boolean)
            permission (dict)
    """
    # vars
    data = validate_permission_data(request.get_json())

    try:
        # create permission
        permission = Permission(**data)
        permission.insert()

        return jsonify({
            "success": True,
            "permission": permission.format()
        })
    except Exception as e:
        abort(400)


@permissions.route("/permissions/<int:permission_id>", methods=['PATCH'])
@requires_auth('update:permissions')
def update_permissions(permission_id):
    """ Update permissions

        Parameters:
            permission_id (int): Id of permission

        Patch data:
            name (string)
            description (string)

        Returns:
            success (boolean)
            permission (dict)
    """
    # vars
    data = validate_permission_update_data(request.get_json())

    # get permission
    permission = Permission.query.first_or_404(permission_id)

    # TODO: implement this
    # can update own permission only
    # if permission.id != auth_permission_id():
    #     abort(403)

    try:
        permission.query.update(data)
        return jsonify({
            "success": True,
            "permission": permission.format()
        })
    except Exception as e:
        abort(400)


@permissions.route(
    "/permissions/<int:permission_id>", methods=['DELETE'])
@requires_auth('delete:permissions')
def delete_permissions(permission_id):
    """ Delete permissions

        Parameters:
            permission_id (int): Id of permission

        Returns:
            success (boolean)
            deleted_id (int)
    """
    # vars
    permission = Permission.query.first_or_404(permission_id)

    # TODO: implement this
    # can delete own permission only
    # if permission.id != auth_permission_id():
    #     abort(403)

    try:
        permission.delete()
        return jsonify({
            "success": True,
            "deleted_id": permission.id
        })
    except Exception as e:
        abort(400)
