from flask import Blueprint, jsonify

from limbook_api.v1.auth.utils import requires_auth

auth = Blueprint('auth', __name__)


# ====================================
# SECURE ROUTES
# ====================================
@auth.route("/secure-route")
@requires_auth('read:secure_route')
def secure():
    """Secure route for testing purpose"""
    return jsonify({
        "success": True
    })
