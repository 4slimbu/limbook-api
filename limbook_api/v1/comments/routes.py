from flask import Blueprint, jsonify, abort, request

from limbook_api.v1.auth.utils import requires_auth, auth_user_id
from limbook_api.v1.comments import Comment, filter_comments, \
    validate_comment_data, validate_comment_create_data

comments = Blueprint('comments', __name__)


# ====================================
# ROUTES
# ====================================
@comments.route("/comments", methods=['GET'])
@requires_auth('read:comments')
def get_comments():
    """ Get all available comments

        Query Parameters:
             search_term (str)
             page (int)
             post_id (int)

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
                comment.format() for comment in filter_comments()
            ],
            'total': filter_comments(count_only=True),
            'query_args': request.args,
        })
    except Exception as e:
        abort(400)


@comments.route("/comments/<int:comment_id>", methods=['GET'])
@requires_auth('read:comments')
def get_comment(comment_id):
    """ Get comment

        Returns:
            success (boolean)
            comment (dict)
    """
    comment = Comment.query.filter(Comment.id == comment_id).first_or_404()
    try:
        return jsonify({
            'success': True,
            'comment': comment.format()
        })
    except Exception as e:
        abort(400)


@comments.route("/comments", methods=['POST'])
@requires_auth('create:comments')
def create_comments():
    """ Create new comments

        Post data:
            post_id (int): Id of post to which comment will belong
            content (string): Content for the comment

        Returns:
            success (boolean)
            comment (dict)
    """
    # vars
    data = request.get_json()

    validate_comment_create_data(data)

    # create comment
    comment = Comment(**{
        'content': data.get('content'),
        'user_id': auth_user_id(),
        'post_id': data.get('post_id')
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
    "/comments/<int:comment_id>", methods=['PATCH'])
@requires_auth('update:comments')
def update_comments(comment_id):
    """ Update comments

        Parameters:
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
    comment = Comment.query.filter(Comment.id == comment_id).first_or_404()

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


@comments.route("/comments/<int:comment_id>", methods=['DELETE'])
@requires_auth('delete:comments')
def delete_comments(comment_id):
    """ Delete comments

        Parameters:
            comment_id (int): Id of comment

        Returns:
            success (boolean)
            deleted_id (int)
    """
    # vars
    comment = Comment.query.filter(Comment.id == comment_id).first_or_404()

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


@comments.route("/comments/<int:comment_id>/replies", methods=['POST'])
@requires_auth('create:comments')
def reply_comments(comment_id):
    """ Reply comments

        Parameters:
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
    comment = Comment.query.filter(Comment.id == comment_id).first_or_404()

    try:
        # reply comment
        reply = Comment(**{
            'content': data.get('content'),
            'parent_id':
                comment.parent_id if comment.parent_id else comment.id,
            'user_id': auth_user_id(),
            'post_id': comment.post_id
        })
        reply.insert()

        return jsonify({
            "success": True,
            "comment": reply.format()
        })
    except Exception as e:
        abort(400)
