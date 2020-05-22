from random import randint

from faker import Faker
from flask import request
from sqlalchemy import or_

from limbook_api.db.utils import filter_model
from limbook_api.errors.validation_error import ValidationError
from limbook_api.v1.permissions import Permission

fake = Faker()


def generate_permission(slug=None, name=None, description=None):
    """Generates new permission with random attributes for testing
    """
    permission = Permission(**{
        'slug': slug if slug else 'manage:' + str(randint(1000, 9999)),
        'name': name if name else 'Manage ' + str(randint(1000, 9999)),
        'description': description if description
        else 'Description ' + str(randint(1000, 9999))
    })

    permission.insert()
    return permission


def validate_permission_data(data):
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
        permission = Permission.query.filter(
            Permission.slug == data.get('slug')
        ).first()
        if permission:
            errors['slug'] = 'Permission slug already exists'

    if len(errors) > 0:
        raise ValidationError(errors)

    return validated_data


def validate_permission_update_data(data):
    data = data if data else {}
    validated_data = {}
    errors = {}

    if data.get('slug'):
        errors['slug'] = 'Permission slug cannot be updated'

    if data.get('name'):
        validated_data['name'] = data.get('name')

    if data.get('description'):
        validated_data['description'] = data.get('description')

    if len(errors) > 0:
        raise ValidationError(errors)

    return validated_data


def filter_permissions(count_only=False):
    query = Permission.query

    # search
    search_term = request.args.get('search_term')
    if search_term:
        query = query.filter(
            or_(
                Permission.slug.ilike("%{}%".format(search_term)),
                Permission.name.ilike("%{}%".format(search_term)),
                Permission.description.ilike("%{}%".format(search_term))
            )
        )

    # return filtered data
    return filter_model(Permission, query, count_only=count_only)
