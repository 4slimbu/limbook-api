from flask import Blueprint

from limbook_api.v1.auth import requires_auth

auth = Blueprint('auth', __name__)


@auth.route("/secure-route")
@requires_auth('read:secure_route')
def secure():
    return 'Secure location accessed'
