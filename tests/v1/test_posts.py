from unittest import main

from flask import json

from limbook_api.v1.image_manager import generate_image, Image
from limbook_api.v1.posts import generate_post, Post
from tests.base import BaseTestCase, test_user_id, api_base


class PostsTestCase(BaseTestCase):
    """This class represents the test case for Posts"""

    # Posts Tests ----------------------------------------
    def test_cannot_access_post_routes_without_correct_permission(self):
        # get posts
        res = self.client().get(
            api_base
            + '/posts?mock_token_verification=True')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # create post
        res = self.client().post(
            api_base
            + '/posts?mock_token_verification=True')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # update post
        res = self.client().patch(
            api_base
            + '/posts/1?mock_token_verification=True')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # delete post
        res = self.client().delete(
            api_base
            + '/posts/1?mock_token_verification=True')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_can_get_posts(self):
        # given
        post = generate_post()

        # make request
        res = self.client().get(
            api_base
            + '/posts'
            + '?mock_token_verification=True&permission=read:posts'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('posts')[0], post.format())

    def test_can_get_posts_with_pagination(self):
        # given
        for i in range(0, 25):
            generate_post()

        # make request
        res = self.client().get(
            api_base
            + '/posts'
            + '?mock_token_verification=True&permission=read:posts'
            + '&page=2'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('posts')), 10)
        self.assertEqual(data.get('total'), 25)
        self.assertEqual(len(data.get('query_args')), 3)

    def test_can_create_posts(self):
        # given
        post = {
            "content": "My new Post"
        }

        # make request
        res = self.client().post(
            api_base
            + '/posts?mock_token_verification=True&permission=create:posts',
            json=post
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            data.get('post').get('content'), post.get('content'))
        self.assertEqual(
            data.get('post').get('user_id'), test_user_id)

    def test_can_create_post_with_images(self):
        # given
        # First user need to upload the image and then attach ids
        # So image id should always be associated with user
        image1 = generate_image(user_id=test_user_id)
        image2 = generate_image(user_id=test_user_id)
        post = {
            "content": "My new Post",
            "image_ids": [image1.id, image2.id]
        }

        # make request
        res = self.client().post(
            api_base
            + '/posts?mock_token_verification=True&permission=create:posts',
            json=post
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            data.get('post').get('content'), post.get('content'))
        self.assertEqual(
            len(data.get('post').get('images')), 2)

    def test_can_update_posts(self):
        # given
        image1 = generate_image(user_id=test_user_id)
        image2 = generate_image(user_id=test_user_id)
        post = generate_post(user_id=test_user_id, images=[image1])
        updated_data = {
            "content": "My Updated Content",
            "image_ids": [image2.id]
        }

        # make request
        res = self.client().patch(
            api_base
            + '/posts/' + str(post.id)
            + '?mock_token_verification=True&permission=update:posts',
            json=updated_data
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            data.get('post').get('content'), updated_data.get('content'))
        self.assertEqual(
            data.get('post').get('images')[0]['id'], image2.id)
        self.assertIsNone(Image.query.get(image1.id))

    def test_can_delete_posts(self):
        # given
        post = generate_post(user_id=test_user_id)

        # make request
        res = self.client().delete(
            api_base
            + '/posts/' + str(post.id)
            + '?mock_token_verification=True&permission=delete:posts'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('deleted_id'), post.id)


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
