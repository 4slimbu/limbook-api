from flask import Blueprint, jsonify, abort, request

from limbook_api.v1.auth import requires_auth, auth_user_id
from limbook_api.v1.comments import Comment, filter_comments, \
    validate_comment_data

comments = Blueprint('comments', __name__)


# ====================================
# ROUTES
# ====================================
@comments.route("/posts/<int:post_id>/comments", methods=['GET'])
@requires_auth('read:comments')
def get_comments(post_id):
    """ Get all available comments

        Query Parameters:
             search_term (str)
             page (int)

        Returns:
            success (boolean)
            comments (list)
            total (int)
            query_args (dict)
    """
    try:
        return jsonify({
            'success': True,
            'comments': [
                comment.format() for comment in filter_comments(post_id)
            ],
            'total': filter_comments(post_id, count_only=True),
            'query_args': request.args,
        })
    except Exception as e:
        abort(400)


@comments.route("/posts/<int:post_id>/comments", methods=['POST'])
@requires_auth('create:comments')
def create_comments(post_id):
    """ Create new comments

        Parameters:
            post_id (int): Id of post to which comment will belong

        Post data:
            content (string): Content for the comment

        Returns:
            success (boolean)
            comment (dict)
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

        return jsonify({
            "success": True,
            "comment": comment.format()
        })
    except Exception as e:
        abort(400)


@comments.route(
    "/posts/<int:post_id>/comments/<int:comment_id>", methods=['PATCH'])
@requires_auth('update:comments')
def update_comments(post_id, comment_id):
    """ Update comments

        Parameters:
            post_id (int): Id of post to which comment belong
            comment_id (int): Id of comment

        Patch data:
            content (string): Content for the comment

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
        return jsonify({
            "success": True,
            "comment": comment.format()
        })
    except Exception as e:
        abort(400)


@comments.route(
    "/posts/<int:post_id>/comments/<int:comment_id>", methods=['DELETE'])
@requires_auth('delete:comments')
def delete_comments(post_id, comment_id):
    """ Delete comments

        Parameters:
            post_id (int): Id of post on which comment was made
            comment_id (int): Id of comment

        Returns:
            success (boolean)
            deleted_id (int)
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
            "deleted_id": comment.id
        })
    except Exception as e:
        abort(400)


@comments.route(
    "/posts/<int:post_id>/comments/<int:comment_id>/replies", methods=['POST'])
@requires_auth('create:comments')
def reply_comments(post_id, comment_id):
    """ Reply comments

        Parameters:
            post_id (int): Id of post on which comment was made
            comment_id (int): Id of comment

        Post Data:
            content (string): reply content

        Returns:
            success (boolean)
            comment: (dict)
    """
    # vars
    data = request.get_json()
    validate_comment_data(data)

    # get comment
    comment = Comment.query.first_or_404(comment_id)

    try:
        # reply comment
        reply = Comment(**{
            'content': data.get('content'),
            'parent_id': comment.parent_id if comment.parent_id else comment.id,
            'user_id': auth_user_id(),
            'post_id': post_id
        })
        reply.insert()

        return jsonify({
            "success": True,
            "comment": reply.format()
        })
    except Exception as e:
        abort(400)
