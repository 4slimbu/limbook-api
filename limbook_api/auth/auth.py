import json
from functools import wraps
from urllib.request import urlopen

from flask import request, abort, current_app
from jose import jwt

from limbook_api.errors.handlers import AuthError

AUTH0_DOMAIN = 'limvus.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffee-shop-auth'


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
    # TODO: find a better solution instead of this hack for testing
    if current_app.config.get('TESTING'):
        if request.args.get('mock_jwt_claim') == 'True':
            return jwt.get_unverified_claims(token)

    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

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
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
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
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)

            if not check_permissions(permission, payload):
                raise AuthError({
                    'code': 'no_permission',
                    'description': 'No Permission'
                }, 401)

            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
