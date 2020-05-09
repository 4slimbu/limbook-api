from flask import Blueprint, render_template, jsonify

from limbook_api.auth.auth import requires_auth, AuthError

main = Blueprint('main', __name__)


@main.route("/")
def home():
    return render_template('home.html')


@main.route("/secure-route")
@requires_auth('get:drinks-detail')
def secure():
    return 'Secure location accessed'

