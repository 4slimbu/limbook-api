from random import randint

from flask import jsonify, abort

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