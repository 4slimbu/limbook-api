from flask import Blueprint, jsonify, abort, request

from limbook_api.auth.auth import requires_auth
from limbook_api.models.comment import Comment

comments = Blueprint('comments', __name__)


def validate_comment_data(data):
    # check if comment attributes are present
    if not data.get('content'):
        abort(422)


def get_all_comments_in_json(post_id):
    # get comments
    comments = Comment.query.filter(Comment.post_id == post_id).all()
    # get count
    comments_count = Comment.query.filter(Comment.post_id == post_id).count()

    # format
    data = []
    for comment in comments:
        data.append(comment.format())

    # return the result
    return jsonify({
        'success': True,
        'comments': data,
        'comments_count': comments_count
    })


# ====================================
# ROUTES
# ====================================
@comments.route("/posts/<int:post_id>/comments", methods=['GET'])
@requires_auth('read:comments')
def get_comments(payload, post_id):
    """ Get all available comments

        Parameters:
             payload (dict): The payload of decoded valid token
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
def create_comments(payload, post_id):
    """ Create new comments

        Parameters:
            payload (dict): The payload of decoded valid token
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
        'user_id': payload.get('sub'),
        'post_id': post_id
    })

    try:
        comment.insert()
        return get_all_comments_in_json(post_id)
    except Exception as e:
        abort(400)


@comments.route("/posts/<int:post_id>/comments/<int:comment_id>", methods=['PATCH'])
@requires_auth('update:comments')
def update_comments(payload, post_id, comment_id):
    """ Update comments

        Parameters:
            payload (dict): The payload of decoded valid token
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
    if comment.user_id != payload.get('sub'):
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
def delete_comments(payload, post_id, comment_id):
    """ Delete comments

        Parameters:
            payload (dict): The payload of decoded valid token
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
    if comment.user_id != payload.get('sub'):
        abort(403)

    try:
        comment.delete()
        return jsonify({
            "success": True,
            "deleted_comment": comment.format()
        })
    except Exception as e:
        abort(400)