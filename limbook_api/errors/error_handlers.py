from flask import jsonify

from limbook_api import AuthError, ImageUploadError
from limbook_api.errors.validation_error import ValidationError


def register_error_handlers(app):
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

    @app.errorhandler(ImageUploadError)
    def image_upload_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "error_code": error.error.get('code'),
            "message": error.error.get('description')
        }), error.status_code

    @app.errorhandler(ValidationError)
    def validation_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "error_code": error.error.get('code'),
            "message": error.error.get('description'),
            "errors": error.error.get('errors')
        }), error.status_code

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "error_code": "unauthorized",
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "error_code": "forbidden",
            "message": "Forbidden"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "error_code": "not_found",
            "message": "Resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "error_code": "unprocessable",
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "error_code": "bad_request",
            "message": "Bad Request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "error_code": "method_not_allowed",
            "message": "Method not allowed"
        }), 405

    @app.errorhandler(413)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 413,
            "error_code": "entity_too_large",
            "message": "Entity too large"
        }), 413

    @app.errorhandler(500)
    def unknown(error):
        return jsonify({
            "success": False,
            "error": 500,
            "error_code": "server_error",
            "message": "Unknown server error"
        }), 500
