from os import abort
from random import randint

from flask import jsonify

from limbook_api.v1.auth import auth_user_id
from limbook_api.v1.image_manager import Image
from limbook_api.v1.posts import Post
from limbook_api.v1.reacts import React


def validate_post_data(data):
    # check if post attributes are present
    if not data.get('content'):
        abort(422)


def get_images_list_using_ids(image_ids):
    images = []
    for image_id in image_ids:
        image = Image.query.filter(
            Image.id == image_id,
            Image.user_id == auth_user_id()
        ).first_or_404()

        images.append(image)

    return images


def get_all_posts_in_json():
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


def validate_react_data(data):
    # check if react attributes are present
    if not data.get('content'):
        abort(422)


def get_all_post_reacts_in_json(post_id, user_id):
    # get reacts
    reacts = React.query.filter(
        React.post_id == post_id,
        React.user_id == user_id
    ).all()

    # get count
    reacts_count = React.query.filter(
        React.post_id == post_id,
        React.user_id == user_id
    ).count()

    # format
    data = []
    for react in reacts:
        data.append(react.format())

    # return the result
    return jsonify({
        'success': True,
        'reacts': data,
        'reacts_count': reacts_count
    })


def generate_post(content=None, user_id=None):
    """Generates new post with random attributes for testing
    """
    post = Post(**{
        'content': content if content else 'Post ' + str(randint(1000, 9999)),
        'user_id': user_id if user_id else str(randint(1000, 9999))
    })

    post.insert()
    return post
