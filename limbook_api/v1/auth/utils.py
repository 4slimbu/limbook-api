from functools import wraps
from functools import wraps
from urllib.request import urlopen

import jwt
from flask import current_app, abort, request, json
from jose import jwt

from limbook_api import AuthError, cache


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
        'sub': "auth0|5eca959e92dce80c6f176d58",
        'is_verified': True,
        'permissions': permission
    }


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

    return int(payload.get('sub'))


def blacklist_token(token):
    # for k in cache.cache._cache:
    #     print(k, cache.get(k))
    cache.set(token, "blacklisted", timeout=60*60)


def is_token_blacklisted(token):
    return cache.get(token) == 'blacklisted'


def user_can(permission):
    payload = current_app.config.get('payload')
    return check_permissions(permission, payload)


def verify_decode_jwt(token):
    """ Verify the jwt token using auth0.

        Parameters:
            token (string): Extracted token from Auth header

        Returns:
            payload (dict): Claims decoded from token

        Raises:
            AuthError: Unable to verify jwt
    """
    auth0_domain = current_app.config.get('AUTH0_DOMAIN')
    algorithms = current_app.config.get('ALGORITHMS')
    api_audience = current_app.config.get('API_AUDIENCE')

    jsonurl = urlopen(f'https://{auth0_domain}/.well-known/jwks.json')
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
