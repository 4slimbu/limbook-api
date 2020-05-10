from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from limbook_api.config import Config
from limbook_api.errors.handlers import AuthError
from limbook_api.db.model import setup_db

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    setup_db(app)

    from limbook_api.main.routes import main
    from limbook_api.posts.routes import posts
    from limbook_api.comments.routes import comments
    from limbook_api.reacts.routes import reacts
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(comments)
    app.register_blueprint(reacts)

    """
    --------------------------------------
    Error handlers for all expected errors
    --------------------------------------
    """

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "error_code": error.error.get('code'),
            "message": error.error.get('description')
        }), error.status_code

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(500)
    def unknown(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Unknown server error"
        }), 500

    return app




