from flask import Blueprint, jsonify, abort

from limbook_api.db.main import Post

posts = Blueprint('posts', __name__, url_prefix='/posts')


# ====================================
# ROUTES
# ====================================
@posts.route("", methods=['GET'])
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
        for post in posts:
            data.append(post.format())

        # return the result
        return jsonify({
            'success': True,
            'posts': data,
            'posts_count': posts_count
        })
    except Exception as e:
        abort(400)
