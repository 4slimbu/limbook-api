from flask import Blueprint, jsonify, abort

from limbook_api.db.main import Post

posts = Blueprint('posts', __name__)


# ====================================
# ROUTES
# ====================================
@posts.route("/", methods=['GET'])
def get_posts():
    """ Get all available posts

        Returns:
            success (boolean)
            posts (list)
            total_posts (int)
    """
    try:
        # get posts
        posts = Post.query.all()
        # get count
        posts_count = Post.query.count()

        # format
        data = []
        for drink in posts:
            data.append(drink.short())

        # return the result
        return jsonify({
            'success': True,
            'posts': data,
            'posts_count': posts_count
        })
    except Exception:
        abort(400)
