from flask import Blueprint, jsonify

from limbook_api.v1.auth.utils import requires_auth
from limbook_api.v1.comments import Comment
from limbook_api.v1.posts import Post

stats = Blueprint('stats', __name__)


# ====================================
# SECURE ROUTES
# ====================================
@stats.route("/stats")
@requires_auth('read:stats')
def get_stats():
    """Get stats"""

    return jsonify({
        "success": True,
        "stats": {
            "posts": Post.query.count(),
            "comments": Comment.query.count()
        }
    })
