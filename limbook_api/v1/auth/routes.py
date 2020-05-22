import secrets
from datetime import datetime, timedelta

from flask import Blueprint, request, jsonify, abort

from limbook_api.v1.auth import AuthError
from limbook_api.v1.auth.utils import validate_register_data, \
    validate_login_data, generate_token, validate_reset_password_data, \
    validate_verify_email_data, refresh_auth_token, requires_auth, \
    blacklist_token, send_verification_mail, send_reset_password_mail, \
    get_token_from_auth_header
from limbook_api.v1.users import User, Role

auth = Blueprint('auth', __name__)


# ====================================
# SECURE ROUTES
# ====================================
@auth.route("/secure-route")
@requires_auth('read:secure_route')
def secure():
    """Secure route for testing purpose"""
    return 'Secure location accessed'


@auth.route("/logout", methods=['POST'])
@requires_auth()
def logout():
    """ Logout

    Puts the access and refresh token of the auth user in
    blacklist so that those tokens cannot be used again.

    Post data:
        refresh_token (string | required)

    Returns:
        success (boolean)
    """
    data = request.get_json()

    blacklist_token(get_token_from_auth_header())
    blacklist_token(data.get('refresh_token'))

    return jsonify({
        "success": True
    })


# ====================================
# PUBLIC ROUTES
# ====================================
@auth.route("/register", methods=['POST'])
def register():
    """ Create new users

        Post data:
            first_name (string | required)
            last_name (string | required)
            email (string | required)
            phone_number (string | optional)
            password (string | required)
            confirm_password (string | required)

        Returns:
            success (boolean)
            user (dict)
    """
    # vars
    data = validate_register_data(request.get_json())

    # create user
    role = Role.query.filter(Role.slug == 'unverified_user').first()
    user = User(**data, role_id=role.id)

    try:
        user.insert()

        # send email
        send_verification_mail(user)

        return jsonify({
            "success": True,
            "user": user.format()
        })
    except Exception as e:
        abort(400)


@auth.route("/login", methods=['POST'])
def login():
    """ Login

        Post data:
            email (string | required)
            password (string |required)

        Returns:
            success (boolean)
            user (dict)
            access_token (string)
            refresh_token (string)
    """
    data = validate_login_data(request.get_json())

    try:
        token = generate_token(data.get('email'), data.get('password'))
        refresh_token = generate_token(
            data.get('email'), data.get('password'), is_refresh_token=True
        )
    except Exception as e:
        raise AuthError({
            'code': 'login_failed',
            'description': 'Unable to login with given credentials'
        }, 401)

    return jsonify({
        "success": True,
        "access_token": token,
        "refresh_token": refresh_token
    })


@auth.route("/send-verification-email", methods=['POST'])
def send_verification_email():
    """ Send verification email

    Post data:
        email (string | required)

    Returns:
        success (boolean) or 400 error
    """
    data = request.get_json()
    user = User.query.filter(User.email == data.get('email')).first_or_404()

    try:
        # send email
        send_verification_mail(user)

        return jsonify({
            "success": True
        })
    except Exception as e:
        abort(400)


@auth.route("/verify-email", methods=['POST'])
def verify_email():
    """ Verify email

    Post data:
        verification_code (string | required)

    Returns:
        success (boolean) or 400 error
    """

    try:
        data = validate_verify_email_data(request.get_json())
        user = User.query.filter(
            User.email_verif_code == data.get('verification_code'),
            User.email_verif_code_expires_on > datetime.utcnow()
        ).first()

        user.email_verified = True
        user.email_verif_code = None
        user.email_verif_code_expires_on = None
        user.update()

        return jsonify({
            "success": True
        })
    except Exception as e:
        abort(400)


@auth.route("/send-reset-password-email", methods=['POST'])
def send_reset_password_email():
    """ Send reset password email

    Post data:
        email (string)

    Returns:
        success (boolean) or 400 error
    """
    data = request.get_json()
    user = User.query.filter(User.email == data.get('email')).first_or_404()

    try:
        # generate verification code
        reset_password_code = secrets.token_hex(8)

        # save it to database
        user.password_reset_code = reset_password_code
        user.password_reset_code_expires_on = datetime.utcnow() + timedelta(
            hours=1)
        user.update()

        # send email
        send_reset_password_mail(user, reset_password_code)

        return jsonify({
            "success": True
        })
    except Exception as e:
        abort(400)


@auth.route("/reset-password", methods=['POST'])
def reset_password():
    """ Reset Password

    Post data:
        password_reset_code (string)
        email (string)
        password (string)
        confirm_password (string)

    Returns:
        success (boolean) or 400 error
    """
    try:
        data = validate_reset_password_data(request.get_json())
        user = User.query.filter(
            User.email == data.get('email'),
            User.password_reset_code == data.get('password_reset_code'),
            User.password_reset_code_expires_on > datetime.utcnow()
        ).first()

        user.password = data.get('password')
        user.update()

        return jsonify({
            "success": True
        })
    except Exception as e:
        abort(400)


@auth.route("/refresh-token", methods=['GET'])
def refresh_token():
    """ Refresh token

    Returns:
        success (boolean)
        access_token (string)
        refresh_token (string)
    """
    tokens = refresh_auth_token()
    return jsonify({
        "success": True,
        "access_token": tokens.get('refresh_token'),
        "refresh_token": tokens.get('refresh_token')
    })
