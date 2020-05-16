import secrets

from faker import Faker
from flask import abort, request
from sqlalchemy import or_

from limbook_api import bcrypt
from limbook_api.db.utils import filter_model
from limbook_api.errors.validation_error import ValidationError
from limbook_api.v1.roles import Role, generate_role
from limbook_api.v1.users import User

fake = Faker()


def generate_user(first_name=None, last_name=None, email=None, password=None):
    """Generates new user with random attributes for testing
    """
    password = password if password else secrets.token_hex(16)
    user = User(**{
        'first_name': first_name if first_name else fake.name().split()[0],
        'last_name': last_name if last_name else fake.name().split()[-1],
        'email': email if email else fake.email(),
        'password': bcrypt.generate_password_hash(password).decode('utf-8'),
        'role_id': generate_role().id
    })

    user.insert()
    return user


def validate_user_data(data):
    validated_data = {}
    errors = {}

    # check first_name
    if data.get('first_name'):
        validated_data['first_name'] = data.get('first_name')
    else:
        errors['first_name'] = 'First name is required'

    # check last_name
    if data.get('last_name'):
        validated_data['last_name'] = data.get('last_name')
    else:
        errors['last_name'] = 'Last name is required'

    # check email
    if data.get('email'):
        validated_data['email'] = data.get('email')
    else:
        errors['email'] = 'Email is required'

    # check role_id
    if data.get('role_id'):
        validated_data['role_id'] = data.get('role_id')
    else:
        errors['role_id'] = 'Role id is required'

    # check password
    if data.get('password'):
        validated_data['password'] = data.get('password')
    else:
        errors['password'] = 'Password is required'

    # check confirm password
    if data.get('confirm_password'):
        pass
    else:
        errors['confirm_password'] = 'Confirm password is required'

    if data.get('confirm_password') != data.get('password'):
        errors['confirm_password'] = 'Password and Confirm password must match'

    if data.get('email'):
        user = User.query.filter(User.email == data.get('email')).first()
        if user:
            errors['email'] = 'Email already exists'

    if data.get('role_id'):
        role = Role.query.filter(Role.id == data.get('role_id')).first()
        if role is None:
            errors['role_id'] = 'Role does not exists'

    # return errors
    if len(errors) > 0:
        raise ValidationError(errors)

    # return validated data
    return validated_data


def validate_user_update_data(data):
    validated_data = {}
    errors = {}

    # check first_name
    if data.get('first_name'):
        validated_data['first_name'] = data.get('first_name')

    # check last_name
    if data.get('last_name'):
        validated_data['last_name'] = data.get('last_name')

    # check email
    if data.get('email'):
        validated_data['email'] = data.get('email')

    # check password
    if data.get('password'):
        validated_data['password'] = data.get('password')

    # check confirm password
    if data.get('confirm_password'):
        validated_data['confirm_password'] = data.get('confirm_password')

        # check if password and confirm password match
        if data.get('confirm_password') != data.get('password'):
            errors['confirm_password'] = 'Password and Confirm password ' \
                                         'must match'

    # check role_id
    if data.get('role_id'):
        validated_data['role_id'] = data.get('role_id')

        # role id must exists
        role = Role.query.filter(Role.id == data.get('role_id')).first()
        if role is None:
            errors['role_id'] = 'Role does not exists'

    # cannot update email
    if data.get('email'):
        errors['email'] = 'Cannot update email'

    # return errors
    if len(errors) > 0:
        raise ValidationError(errors)

    # return validated data
    return validated_data


def filter_users(count_only=False):
    query = User.query

    # search
    search_term = request.args.get('search_term')
    if search_term:
        query = query.filter(
            or_(
                User.first_name.ilike("%{}%".format(search_term)),
                User.last_name.ilike("%{}%".format(search_term)),
                User.email.ilike("%{}%".format(search_term))
            )
        )

    # return filtered data
    return filter_model(User, query, count_only=count_only)
