import secrets
from datetime import datetime, timedelta

import jwt
from flask import current_app, abort, request

from limbook_api import bcrypt, AuthError
from limbook_api.v1.users import User, ValidationError


def validate_register_data(data):
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

    # check password
    if data.get('password'):
        password = data.get('password')
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

    # return errors
    if len(errors) > 0:
        raise ValidationError(errors)

    # secure password
    validated_data['password'] = bcrypt.generate_password_hash(
        password
    ).decode('utf-8')

    # return validated data
    return validated_data


def validate_login_data(data):
    validated_data = {}
    errors = {}

    # check email
    if data.get('email'):
        validated_data['email'] = data.get('email')
    else:
        errors['email'] = 'Email is required'

    # check password
    if data.get('password'):
        validated_data['password'] = data.get('password')
    else:
        errors['password'] = 'Password is required'

    # return errors
    if len(errors) > 0:
        raise ValidationError(errors)

    # return validated data
    return validated_data


def validate_verify_email_data(data):
    validated_data = {}
    errors = {}

    # check email
    if data.get('verification_code'):
        validated_data['verification_code'] = data.get('verification_code')
    else:
        errors['verification_code'] = 'Verification code is required'

    # return errors
    if len(errors) > 0:
        raise ValidationError(errors)

    # return validated data
    return validated_data


def validate_reset_password_data(data):
    validated_data = {}
    errors = {}

    # check password reset code
    if data.get('password_reset_code'):
        validated_data['password_reset_code'] = data.get('password_reset_code')
    else:
        errors['password_reset_code'] = 'Password reset code is required'
        
    # check email
    if data.get('email'):
        validated_data['email'] = data.get('email')
    else:
        errors['email'] = 'Email is required'

    # check password
    if data.get('password'):
        password = data.get('password')
    else:
        errors['password'] = 'Password is required'

    # check confirm password
    if data.get('confirm_password'):
        pass
    else:
        errors['confirm_password'] = 'Confirm Password is required'

    # confirm password and password must match
    if data.get('confirm_password') != data.get('password'):
        errors['confirm_password'] = 'Password and Confirm password must match'

    # return errors
    if len(errors) > 0:
        raise ValidationError(errors)

    # secure password
    validated_data['password'] = bcrypt.generate_password_hash(
        password
    ).decode('utf-8')

    # return validated data
    return validated_data


def generate_token(email, password, is_refresh_token=False):
    """Generate token

    Generates token or refresh token if user with given email and
    password exists in the database

    Returns:
        token (string) or None
    """
    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        if is_refresh_token:
            valid_seconds = current_app.config.get('REFRESH_TOKEN_VALID_TIME')
            return encode_auth_token(user, valid_seconds=valid_seconds)
        else:
            valid_seconds = current_app.config.get('ACCESS_TOKEN_VALID_TIME')
            return encode_auth_token(user, valid_seconds=valid_seconds)

    else:
        return None


def encode_auth_token(user, valid_seconds):
    """
    Generates the Auth Token

    Returns:
        token (string)
    """
    try:
        payload = {
            'exp': datetime.utcnow() + timedelta(seconds=valid_seconds),
            'iat': datetime.utcnow(),
            'sub': user.id,
            'permissions': user.format().get('permissions'),
            # while testing, tokens are generated in quick succession and
            # for same payload, it is not possible to differentiate them
            # so this rand key helps to generate different token.
            'rand': secrets.token_hex(4)
        }
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        ).decode('utf-8')
    except Exception as e:
        abort(500)


def get_token_from_auth_header():
    """ Extract token from the authorization header. """

    if 'Authorization' not in request.headers:
        abort(401)

    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')

    if len(header_parts) != 2:
        abort(401)
    elif header_parts[0].lower() != 'bearer':
        abort(401)

    return header_parts[1]


def refresh_auth_token():
    """Refresh tokens

    Extract token from request header and if it's valid,
    blacklist the token and generate new token

    Returns:
        token (string)
    """
    try:
        token = get_token_from_auth_header()

        # TODO: blacklist token

        payload = decode_token(token)

        user = User.query.get(payload.get('sub'))

        if user is None:
            abort(400)

        valid_seconds = current_app.config.get('REFRESH_TOKEN_VALID_TIME')
        return encode_auth_token(user, valid_seconds=valid_seconds)

    except Exception as e:
        abort(400)


def decode_token(token):
    """
    Decodes the auth token

    Parameters:
        token (string)

    Returns:
        payload (dict)
    """
    try:
        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
        return payload

    except jwt.ExpiredSignatureError:
        raise AuthError({
            'code': 'token_expired',
            'description': 'Token expired'
        }, 401)

    except Exception as e:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to parse authentication token.'
        }, 400)

