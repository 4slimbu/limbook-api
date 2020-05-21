from flask import Blueprint, jsonify, abort, request

from limbook_api.v1.auth.utils import requires_auth, auth_user_id
from limbook_api.v1.posts import Post
from limbook_api.v1.reacts import React, filter_reacts

reacts = Blueprint('reacts', __name__)


# ====================================
# ROUTES
# ====================================
@reacts.route("/posts/<int:post_id>/reacts", methods=['GET'])
@requires_auth('read:reacts')
def get_post_reacts(post_id):
    """ Get all available reacts

        Parameters:
             post_id (int): Id of post to which reacts belong to

        Returns:
            success (boolean)
            reacts (list)
            total (int)
            query_args (dict)
    """
    try:
        return jsonify({
            'success': True,
            'reacts': [
                react.format() for react in filter_reacts(post_id)
            ],
            'total': filter_reacts(post_id, count_only=True),
            'query_args': request.args,
        })
    except Exception as e:
        abort(400)


@reacts.route("/posts/<int:post_id>/reacts/toggle", methods=['POST'])
@requires_auth(['create:reacts', 'update:reacts'])
def toggle_post_reacts(post_id):
    """ Create new react or delete if exist

        Parameters:
            post_id (int): Id of post to which react will belong

        Returns:
            success (boolean)
            react (list)
    """
    try:

        post = Post.query.filter(Post.id == post_id).first_or_404()

        user_react = React.query.filter(
            React.post_id == post_id,
            React.user_id == auth_user_id()
        ).one_or_none()

        # toggle react
        if user_react is None:
            # create react
            react = React(**{
                'user_id': auth_user_id(),
                'post_id': post_id
            })
            react.insert()
        else:
            # delete
            user_react.delete()

        return jsonify({
            "success": True,
            "post": post.format()
        })

    except Exception as e:
        abort(400)
