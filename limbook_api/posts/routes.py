from flask import Blueprint, jsonify, abort, request

from limbook_api.auth import requires_auth, auth_user_id
from limbook_api.image_manager import Image
from limbook_api.posts import Post
from limbook_api.reacts import React

posts = Blueprint('posts', __name__)


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


# ====================================
# ROUTES
# ====================================
@posts.route("/posts", methods=['GET'])
@requires_auth('read:posts')
def get_posts():
    """ Get all available posts

        Returns:
            success (boolean)
            posts (list)
            total_posts (int)
    """
    try:
        return get_all_posts_in_json()
    except Exception as e:
        abort(400)


@posts.route("/posts", methods=['POST'])
@requires_auth('create:posts')
def create_posts():
    """ Create new posts

        Internal Parameters:
            content (string): Content for the post
            user_id (string): Internal parameter extracted from current_user

        Returns:
            success (boolean)
            posts (list)
            total_posts (int)
    """
    # vars
    data = request.get_json()

    validate_post_data(data)

    # create post
    post = Post(**{
        'content': data.get('content'),
        'user_id': auth_user_id()
    })

    try:
        post.insert()
        return get_all_posts_in_json()
    except Exception as e:
        abort(400)


@posts.route("/posts/<int:post_id>", methods=['PATCH'])
@requires_auth('update:posts')
def update_posts(post_id):
    """ Update posts

        Parameters:
            post_id (int): Id of post

        Internal Parameters:
            content (string): Content for the post
            user_id (string): Internal parameter extracted from current_user

        Returns:
            success (boolean)
            posts (list)
            total_posts (int)
    """
    # vars
    data = request.get_json()

    validate_post_data(data)

    # get post
    post = Post.query.first_or_404(post_id)

    # can update own post only
    if post.user_id != auth_user_id():
        abort(403)

    # update post
    post.content = data.get('content')

    try:
        post.update()
        return get_all_posts_in_json()
    except Exception as e:
        abort(400)


@posts.route("/posts/<int:post_id>", methods=['DELETE'])
@requires_auth('delete:posts')
def delete_posts(post_id):
    """ Delete posts

        Parameters:
            post_id (int): Id of post

        Internal Parameters:
            user_id (string): Internal parameter extracted from current_user

        Returns:
            success (boolean)
            deleted_post (dict)
    """
    # vars
    post = Post.query.first_or_404(post_id)

    # can delete own post only
    if post.user_id != auth_user_id():
        abort(403)

    try:
        # delete images
        for image in post.images:
            image.delete()

        # delete post
        post.delete()

        return jsonify({
            "success": True,
            "deleted_post": post.format()
        })
    except Exception as e:
        abort(400)


@posts.route("/posts/<int:post_id>/images", methods=['POST'])
@requires_auth('update:posts')
def attach_images_to_post(post_id):
    """ Attach images to post

        Parameters:
            post_id (int): Id of post

        Internal Parameters:
            image_ids (list): List of image ids

        Returns:
            success (boolean)
            post (dict)
    """
    # vars
    post = Post.query.first_or_404(post_id)

    # can attach images to own post only
    if post.user_id != auth_user_id():
        abort(403)

    # attach images
    data = request.get_json()
    image_ids = data.get('image_ids')
    images = get_images_list_using_ids(image_ids)

    try:
        post.images = images
        post.update()
        return jsonify({
            "success": True,
            "post": post.format()
        })
    except Exception as e:
        abort(400)


@posts.route("/posts/<int:post_id>/reacts", methods=['GET'])
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


@posts.route("/posts/<int:post_id>/reacts/toggle", methods=['POST'])
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