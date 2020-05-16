import secrets

from faker import Faker
from flask import abort, request
from sqlalchemy import or_

from limbook_api import bcrypt
from limbook_api.db.utils import filter_model
from limbook_api.errors.validation_error import ValidationError
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
        'password': bcrypt.generate_password_hash(password).decode('utf-8')
    })

    user.insert()
    return user


def validate_user_data(data):
    errors = {}
    # check if user attributes are present
    if not data.get('first_name'):
        errors['first_name'] = 'First name is required'

    if not data.get('last_name'):
        errors['last_name'] = 'Last name is required'

    if not data.get('email'):
        errors['email'] = 'Email is required'

    if not data.get('password'):
        errors['password'] = 'Password is required'

    if not data.get('confirm_password'):
        errors['confirm_password'] = 'Confirm password is required'

    if data.get('confirm_password') != data.get('password'):
        errors['confirm_password'] = 'Password and Confirm password must match'

    if data.get('email'):
        user = User.query.filter(User.email == data.get('email')).first()
        if user:
            errors['email'] = 'Email already exists'

    if len(errors) > 0:
        raise ValidationError(errors)


def validate_user_update_data(data):
    validated_data = {}
    errors = {}

    # check if user attributes are present
    if data.get('first_name'):
        validated_data['first_name'] = data.get('first_name')

    if data.get('last_name'):
        validated_data['last_name'] = data.get('last_name')

    if data.get('email'):
        validated_data['email'] = data.get('email')

    if data.get('password'):
        validated_data['password'] = data.get('password')

    if data.get('confirm_password'):
        validated_data['confirm_password'] = data.get('confirm_password')
        if data.get('confirm_password') != data.get('password'):
            errors['confirm_password'] = 'Password and Confirm password ' \
                                         'must match'

    if data.get('email'):
        errors['email'] = 'Cannot update email'

    if len(errors) > 0:
        raise ValidationError(errors)

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
