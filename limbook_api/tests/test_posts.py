from unittest import main

from flask import json

from limbook_api.models.post import create_post
from limbook_api.tests.base import BaseTestCase, test_user_id


class PostsTestCase(BaseTestCase):
    """This class represents the test case for Posts"""

    # Posts Tests ----------------------------------------
    def test_cannot_access_post_routes_without_correct_permission(self):
        # get posts
        res1 = self.client().get(
            '/posts?mock_token_verification=True')
        data1 = json.loads(res1.data)

        # create post
        res2 = self.client().post(
            '/posts?mock_token_verification=True')
        data2 = json.loads(res2.data)

        # update post
        res3 = self.client().patch(
            '/posts/1?mock_token_verification=True')
        data3 = json.loads(res3.data)

        # delete post
        res4 = self.client().delete(
            '/posts/1?mock_token_verification=True')
        data4 = json.loads(res4.data)

        # assert
        self.assertEqual(res1.status_code, 401)
        self.assertEqual(data1.get('error_code'), 'no_permission')
        self.assertEqual(res2.status_code, 401)
        self.assertEqual(data2.get('error_code'), 'no_permission')
        self.assertEqual(res3.status_code, 401)
        self.assertEqual(data3.get('error_code'), 'no_permission')
        self.assertEqual(res4.status_code, 401)
        self.assertEqual(data4.get('error_code'), 'no_permission')

    def test_can_get_posts(self):
        # given
        post = create_post()

        # make request
        res = self.client().get(
            '/posts'
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
            '/posts?mock_token_verification=True&permission=create:posts',
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
        post = create_post({
            "content": "My new post",
            "user_id": test_user_id
        })
        updated_post_content = {
            "content": "My Updated Content"
        }

        # make request
        res = self.client().patch(
            '/posts/' + str(post.id)
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
        post = create_post({
            'content': 'My new post',
            'user_id': test_user_id
        })

        # make request
        res = self.client().delete(
            '/posts/' + str(post.id)
            + '?mock_token_verification=True&permission=delete:posts'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('deleted_post'), post.format())


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
