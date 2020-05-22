import secrets
from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import current_app, abort, request
from flask_mail import Message
from jose import jwt

from limbook_api import bcrypt, AuthError, cache, mail, q
from limbook_api.v1.users import User, ValidationError


def mock_token_verification(permission=None):
    """ Mock payload with custom permission

        Parameters:
            permission (string): e.g: "read:posts,create:posts"

        returns:
            payload (dict)
    """
    if permission is None:
        permission = []
    else:
        permission = permission.split(',')

    return {
        'iat': 1589041232,
        'exp': 1589048432,
        'sub': 1,
        'is_verified': True,
        'permissions': permission
    }


def validate_register_data(data):
    data = data if data else {}
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
    data = data if data else {}
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
    data = data if data else {}
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
    data = data if data else {}
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
            'sub': str(user.id),
            'is_verified': user.email_verified,
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
        )
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
        tokens (dict): new access and refresh token
    """
    token = get_token_from_auth_header()

    payload = decode_token(token)

    user = User.query.get(payload.get('sub'))

    if user is None:
        abort(400)

    blacklist_token(token)
    valid_seconds = current_app.config.get('ACCESS_TOKEN_VALID_TIME')
    access_token = encode_auth_token(user, valid_seconds=valid_seconds)
    valid_seconds = current_app.config.get('REFRESH_TOKEN_VALID_TIME')
    refresh_token = encode_auth_token(user, valid_seconds=valid_seconds)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }




def decode_token(token):
    """
    Decodes the auth token

    Parameters:
        token (string)

    Returns:
        payload (dict)
    """
    if is_token_blacklisted(token):
        raise AuthError({
            'code': 'token_blacklisted',
            'description': 'Token access has been revoked'
        }, 401)

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
        }, 401)


def check_permissions(required_permission, payload):
    """ Check if required permission exists in the verified token's payload.

        Parameters:
            required_permission (string|list):
                A string describing the type of permission.
                e.g: get:drinks, post:drinks, ['get:drinks', 'manage:drinks']
            payload (dict): Extracted token claims containing the allowed
                permissions for the user.

        Returns:
            boolean: Whether user has the permission or not.
    """
    if required_permission == '':
        return True

    if isinstance(required_permission, str):
        required_permission = [required_permission]

    user_permissions = payload.get('permissions')
    if user_permissions and \
            len(list(set(required_permission) & set(user_permissions))) > 0:
        return True

    return False


def requires_auth(permission=''):
    """ Decorator method to check if user can access the resource.

        Parameters:
            permission (string): permission (i.e. 'post:drinks')

        Returns:
            function: Wrapped function with payload passed as argument.

        Raises:
            AuthError: Unable to provide access
    """

    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            # TODO: find a better solution instead of this hack for testing
            if current_app.config.get('TESTING') \
                    and request.args.get('mock_token_verification') == 'True':
                payload = mock_token_verification(
                    permission=request.args.get('permission')
                )
            else:
                token = get_token_from_auth_header()

                payload = decode_token(token)

            current_app.config['payload'] = payload

            if not payload.get('is_verified'):
                raise AuthError({
                    'code': 'user_not_verified',
                    'description': 'Please verify your email.'
                }, 401)

            if not check_permissions(permission, payload):
                raise AuthError({
                    'code': 'no_permission',
                    'description': 'No Permission'
                }, 401)

            return f(*args, **kwargs)

        return wrapper

    return requires_auth_decorator


def auth_user_id():
    payload = current_app.config.get('payload')
    if payload is None:
        abort(401)

    return int(payload.get('sub'))


def blacklist_token(token):
    # for k in cache.cache._cache:
    #     print(k, cache.get(k))
    cache.set(token, "blacklisted", timeout=60*60)


def is_token_blacklisted(token):
    return cache.get(token) == 'blacklisted'


def send_verification_mail(user):
    # generate verification code
    verification_code = secrets.token_hex(8)

    # save it to database
    user.email_verif_code = verification_code
    user.email_verif_code_expires_on = datetime.utcnow() + timedelta(hours=1)
    user.update()

    # send mail
    msg = Message(
        'Verify Email Request',
        sender='noreply@demo.com',
        recipients=[user.email]
    )
    msg.body = f'''Please use this token to verify: 
    { verification_code }

    If you did not make this request then simply ignore this email.
    '''
    if current_app.config.get('USE_REDIS'):
        q.enqueue(send_mail, msg)
    else:
        mail.send(msg)


def send_mail(msg):
    from run import app
    with app.app_context():
        mail.send(msg)


def send_reset_password_mail(user, reset_password_code):
    msg = Message(
        'Password Reset Request',
        sender='noreply@demo.com',
        recipients=[user.email]
    )
    msg.body = f'''Please use this token to reset your password: 
    { reset_password_code }

    If you did not make this request then simply ignore this email.
    '''
    if current_app.config.get('USE_REDIS'):
        q.enqueue(send_mail, msg)
    else:
        mail.send(msg)


def validate_profile_data(data):
    data = data if data else {}
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
        errors['email'] = 'Email address cannot be changed.'

    # check password
    if data.get('password'):
        validated_data['password'] = data.get('password')

        # check if password and confirm password match
        if data.get('confirm_password') != data.get('password'):
            errors['confirm_password'] = 'Password and Confirm password ' \
                                         'must match'

    # check profile picture
    if data.get('profile_picture'):
        validated_data['profile_picture'] = data.get('profile_picture')

    # check cover picture
    if data.get('cover_picture'):
        validated_data['cover_picture'] = data.get('cover_picture')

    # return errors
    if len(errors) > 0:
        raise ValidationError(errors)

    # return validated data
    return validated_data


def user_can(permission):
    payload = current_app.config.get('payload')
    return check_permissions(permission, payload)
