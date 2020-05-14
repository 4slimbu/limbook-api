from flask import Blueprint, jsonify, abort, request

from limbook_api.auth import requires_auth, auth_user_id
from limbook_api.comments import Comment, get_all_comments_in_json, \
    validate_comment_data

comments = Blueprint('comments', __name__)


# ====================================
# ROUTES
# ====================================
@comments.route("/posts/<int:post_id>/comments", methods=['GET'])
@requires_auth('read:comments')
def get_comments(post_id):
    """ Get all available comments

        Parameters:
             post_id (int): Id of post to which comments belong to

        Returns:
            success (boolean)
            comments (list)
            total_comments (int)
    """
    try:
        return get_all_comments_in_json(post_id)
    except Exception as e:
        abort(400)


@comments.route("/posts/<int:post_id>/comments", methods=['POST'])
@requires_auth('create:comments')
def create_comments(post_id):
    """ Create new comments

        Parameters:
            post_id (int): Id of post to which comment will belong

        Internal Parameters:
            content (string): Content for the comment
            user_id (string): Internal parameter extracted from current_user

        Returns:
            success (boolean)
            comments (list)
            total_comments (int)
    """
    # vars
    data = request.get_json()

    validate_comment_data(data)

    # create comment
    comment = Comment(**{
        'content': data.get('content'),
        'user_id': auth_user_id(),
        'post_id': post_id
    })

    try:
        comment.insert()
        return get_all_comments_in_json(post_id)
    except Exception as e:
        abort(400)


@comments.route("/posts/<int:post_id>/comments/<int:comment_id>", methods=['PATCH'])
@requires_auth('update:comments')
def update_comments(post_id, comment_id):
    """ Update comments

        Parameters:
            post_id (int): Id of post to which comment belong
            comment_id (int): Id of comment

        Internal Parameters:
            content (string): Content for the comment
            user_id (string): Internal parameter extracted from current_user

        Returns:
            success (boolean)
            comments (list)
            total_comments (int)
    """
    # vars
    data = request.get_json()

    validate_comment_data(data)

    # get comment
    comment = Comment.query.first_or_404(comment_id)

    # can update own comment only
    if comment.user_id != auth_user_id():
        abort(403)

    # update comment
    comment.content = data.get('content')

    try:
        comment.update()
        return get_all_comments_in_json(post_id)
    except Exception as e:
        abort(400)


@comments.route("/posts/<int:post_id>/comments/<int:comment_id>", methods=['DELETE'])
@requires_auth('delete:comments')
def delete_comments(post_id, comment_id):
    """ Delete comments

        Parameters:
            post_id (int): Id of post on which comment was made
            comment_id (int): Id of comment

        Internal Parameters:
            user_id (string): Internal parameter extracted from current_user

        Returns:
            success (boolean)
            comments: (list)
            deleted_comment (dict)
    """
    # vars
    comment = Comment.query.first_or_404(comment_id)

    # can delete own comment only
    if comment.user_id != auth_user_id():
        abort(403)

    try:
        comment.delete()
        return jsonify({
            "success": True,
            "deleted_comment": comment.format()
        })
    except Exception as e:
        abort(400)
