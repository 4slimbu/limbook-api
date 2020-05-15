from unittest import main

from flask import json

from limbook_api.v1.posts import generate_post
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
        self.assertEqual(data.get('posts')[0]['content'], post['content'])
        self.assertEqual(
            data.get('posts')[0]['user_id'],
            test_user_id
        )

    def test_can_update_posts(self):
        # given
        post = generate_post(user_id=test_user_id)
        updated_post_content = {
            "content": "My Updated Content"
        }

        # make request
        res = self.client().patch(
            api_base
            + '/posts/' + str(post.id)
            + '?mock_token_verification=True&permission=update:posts',
            json=updated_post_content
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            data.get('posts')[0]['content'],
            updated_post_content['content']
        )

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
        self.assertEqual(data.get('deleted_post'), post.format())


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
