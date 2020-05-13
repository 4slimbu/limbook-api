import json
from functools import wraps
from urllib.request import urlopen

from flask import request, abort, current_app
from jose import jwt

from limbook_api.errors import AuthError
from limbook_api.tests.base import mock_token_verification


def get_token_auth_header():
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


def check_permissions(permission, payload):
    """ Check if required permission exists in the verified token's payload.

        Parameters:
            permission (string): A string describing the type of permission.
                e.g: get:drinks, post:drinks
            payload (dict): Extracted token claims containing the allowed
                permissions for the user.

        Returns:
            boolean: Whether user has the permission or not.
    """
    permissions = payload.get('permissions')
    if permissions and permission in permissions:
        return True

    return False


def verify_decode_jwt(token):
    """ Verify the jwt token using auth0.

        Parameters:
            token (string): Extracted token from Auth header

        Returns:
            payload (dict): Claims decoded from token

        Raises:
            AuthError: Unable to verify jwt
    """
    # Init
    auth0_domain = current_app.config.get('AUTH0_DOMAIN')
    algorithms = current_app.config.get('ALGORITHMS')
    api_audience = current_app.config.get('API_AUDIENCE')

    json_url = urlopen(f'https://{auth0_domain}/.well-known/jwks.json')
    jwks = json.loads(json_url.read())

    # Get the data in the header
    unverified_header = jwt.get_unverified_header(token)

    # choose our key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            # use the key to validate the jwt
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=algorithms,
                audience=api_audience,
                issuer='https://' + auth0_domain + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please check '
                               'the audience and issuer.'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.'
    }, 400)


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
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)

            current_app.config['payload'] = payload

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

    return payload.get('sub')
