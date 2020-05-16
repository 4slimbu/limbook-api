from random import randint

from flask import jsonify, abort, request

from limbook_api.db.utils import filter_model
from limbook_api.v1.auth import auth_user_id
from limbook_api.v1.comments import Comment


def generate_comment(content=None, user_id=None, post_id=None):
    """Generates new comment with random attributes for testing
    """
    comment = Comment(**{
        'content': content if content else 'Comment' + str(randint(1000, 9999)),
        'user_id': user_id if user_id else str(randint(1000, 9999)),
        'post_id': post_id if post_id else randint(1000, 9999),
    })

    comment.insert()
    return comment


def validate_comment_data(data):
    # check if comment attributes are present
    if not data.get('content'):
        abort(422)


def filter_comments(post_id, count_only=False):
    query = Comment.query

    # search
    search_term = request.args.get('search_term')
    if search_term:
        query = query.filter(Comment.content.ilike("%{}%".format(search_term)))

    # comment belongs to post
    query = query.filter(Comment.post_id == post_id)

    # return filtered data
    return filter_model(Comment, query, count_only=count_only)
