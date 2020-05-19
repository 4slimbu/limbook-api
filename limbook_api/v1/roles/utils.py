from random import randint

from faker import Faker
from flask import request
from sqlalchemy import or_

from limbook_api.db.utils import filter_model
from limbook_api.errors.validation_error import ValidationError
from limbook_api.v1.permissions import Permission, generate_permission
from limbook_api.v1.roles import Role

fake = Faker()


def generate_role(slug=None, name=None, description=None, permissions=None):
    """Generates new role with random attributes for testing
    """
    role = Role(**{
        'slug': slug if slug else 'role_' + str(randint(1000, 9999)),
        'name': name if name else 'Role ' + str(randint(1000, 9999)),
        'description': description if description
        else 'Description ' + str(randint(1000, 9999)),
        'permissions': permissions if permissions
        else [generate_permission(), generate_permission()]
    })

    role.insert()
    return role


def validate_role_data(data):
    data = data if data else {}
    validated_data = {}
    errors = {}

    if data.get('slug'):
        validated_data['slug'] = data.get('slug')
    else:
        errors['slug'] = 'Slug is required'

    if data.get('name'):
        validated_data['name'] = data.get('name')
    else:
        errors['name'] = 'Name is required'

    if data.get('description'):
        validated_data['description'] = data.get('description')
    else:
        errors['description'] = 'Description is required'

    if data.get('slug'):
        role = Role.query.filter(Role.slug == data.get('slug')).first()
        if role:
            errors['slug'] = 'Role slug already exists'

    if len(errors) > 0:
        raise ValidationError(errors)

    return validated_data


def validate_role_update_data(data):
    data = data if data else {}
    validated_data = {}
    errors = {}

    if data.get('slug'):
        errors['slug'] = 'Role slug cannot be updated'

    if data.get('name'):
        validated_data['name'] = data.get('name')

    if data.get('description'):
        validated_data['description'] = data.get('description')

    if len(errors) > 0:
        raise ValidationError(errors)

    return validated_data


def filter_roles(count_only=False):
    query = Role.query

    # search
    search_term = request.args.get('search_term')
    if search_term:
        query = query.filter(
            or_(
                Role.slug.ilike("%{}%".format(search_term)),
                Role.name.ilike("%{}%".format(search_term)),
                Role.description.ilike("%{}%".format(search_term))
            )
        )

    # return filtered data
    return filter_model(Role, query, count_only=count_only)


def get_permission_list_using_ids(permission_ids):
    permissions = []
    for permission_id in permission_ids:
        permission = Permission.query.filter(
            Permission.id == permission_id
        ).first_or_404()

        permissions.append(permission)

    return permissions