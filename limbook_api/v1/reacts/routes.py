from flask import Blueprint, jsonify, abort

from limbook_api.v1.auth import requires_auth, auth_user_id
from limbook_api.v1.posts import Post, get_all_post_reacts_in_json
from limbook_api.v1.reacts import React

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
            total_reacts (int)
    """
    try:
        return get_all_post_reacts_in_json(post_id)
    except Exception as e:
        abort(400)


@reacts.route("/posts/<int:post_id>/reacts/toggle", methods=['POST'])
# TODO: fix caps on Create:reacts and use it
@requires_auth('update:reacts')
def create_post_reacts(post_id):
    """ Create new react or delete if exist

        Parameters:
            post_id (int): Id of post to which react will belong

        Internal Parameters:
            user_id (string): Internal parameter extracted from current_user

        Returns:
            success (boolean)
            reacts (list)
            total_reacts (int)
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
            })
            post.reacts = [react]
            post.update()
        else:
            # delete
            user_react.delete()

        return jsonify({
            "success": True,
            "post": post.format()
        })

    except Exception as e:
        abort(400)
