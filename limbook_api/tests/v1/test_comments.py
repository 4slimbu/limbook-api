from unittest import main

from flask import json

from limbook_api.v1.comments import generate_comment
from limbook_api.v1.posts import generate_post
from limbook_api.tests.base import BaseTestCase
from limbook_api.tests.v1 import test_user_id, api_base


class CommentsTestCase(BaseTestCase):
    """This class represents the test case for Comments"""

    # Comments Tests ----------------------------------------
    def test_cannot_access_comment_routes_without_correct_permission(self):
        # get comments
        res = self.client().get(
            api_base
            + '/posts/1/comments?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # create comment
        res = self.client().post(
            api_base
            + '/posts/1/comments?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # update comment
        res = self.client().patch(
            api_base
            + '/posts/1/comments/1?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # delete comment
        res = self.client().delete(
            api_base
            + '/posts/1/comments/1?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # reply comment
        res = self.client().post(
            api_base
            + '/posts/1/comments/1/replies?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_can_get_comments(self):
        # given
        post = generate_post()
        comment = generate_comment(
            user_id=test_user_id,
            post_id=post.id
        )

        # make request
        res = self.client().get(
            api_base
            + '/posts/' + str(post.id) + '/comments'
            + '?mock_token_verification=True&permission=read:comments'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('comments')[0], comment.format())

    def test_can_create_comments(self):
        # given
        post = generate_post()
        post_id = post.id
        comment = {"content": "My new Comment"}

        # make request
        res = self.client().post(
            api_base
            + '/posts/' + str(post.id) + '/comments'
            + '?mock_token_verification=True&permission=create:comments',
            json=comment
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('comments')[0]['content'], comment['content'])
        self.assertEqual(
            data.get('comments')[0]['user_id'],
            test_user_id
        )
        self.assertEqual(
            data.get('comments')[0]['post_id'],
            post_id
        )

    def test_can_update_comments(self):
        # given
        post = generate_post()
        comment = generate_comment(
            user_id=test_user_id,
            post_id=post.id
        )
        updated_comment_content = {
            "content": "My Updated Content"
        }

        # make request
        res = self.client().patch(
            api_base
            + '/posts/' + str(post.id) + '/comments/' + str(comment.id)
            + '?mock_token_verification=True&permission=update:comments',
            json=updated_comment_content
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            data.get('comments')[0]['content'],
            updated_comment_content['content']
        )

    def test_can_delete_comments(self):
        # given
        post = generate_post()
        comment = generate_comment(
            user_id=test_user_id,
            post_id=post.id
        )

        # make request
        res = self.client().delete(
            api_base
            + '/posts/' + str(post.id) + '/comments/' + str(comment.id)
            + '?mock_token_verification=True&permission=delete:comments'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('deleted_comment'), comment.format())

    def test_can_reply_to_comment(self):
        # given
        post = generate_post()
        post_id = post.id
        comment = generate_comment(post_id=post_id)
        comment_id = comment.id

        reply = {
            "content": "My Reply"
        }

        # reply to comment
        res = self.client().post(
            api_base
            + '/posts/' + str(post_id)
            + '/comments/' + str(comment_id) + '/replies'
            + '?mock_token_verification=True&permission=create:comments',
            json=reply
        )
        data = json.loads(res.data)

        # assert
        expected_reply = {
            **reply,
            "user_id": test_user_id,
            "post_id": post_id,
            "parent_id": comment_id
        }
        self.assertEqual(res.status_code, 200)
        self.assertTrue(expected_reply.items() <= data.get('reply').items())

    def test_reply_are_one_level_deep(self):
        """
        If you reply to reply, then it will be reply to top level comment.
        """
        # given
        post = generate_post()
        post_id = post.id
        comment = generate_comment(post_id=post_id)
        comment_id = comment.id

        reply = {"content": "My Reply"}

        # reply to comment
        res = self.client().post(
            api_base
            + '/posts/' + str(post_id)
            + '/comments/' + str(comment_id) + '/replies'
            + '?mock_token_verification=True&permission=create:comments',
            json=reply
        )
        data = json.loads(res.data)

        # assert
        self.assertTrue(data.get('reply').get('parent_id') == comment_id)

        # reply to reply
        res = self.client().post(
            api_base
            + '/posts/' + str(post_id)
            + '/comments/' + str(data.get('reply').get('id')) + '/replies'
            + '?mock_token_verification=True&permission=create:comments',
            json=reply
        )
        data = json.loads(res.data)

        # assert
        self.assertTrue(data.get('reply').get('parent_id') == comment_id)

        # reply to reply of reply
        res = self.client().post(
            api_base
            + '/posts/' + str(post_id)
            + '/comments/' + str(data.get('reply').get('id')) + '/replies'
            + '?mock_token_verification=True&permission=create:comments',
            json=reply
        )
        data = json.loads(res.data)

        # assert
        self.assertTrue(data.get('reply').get('parent_id') == comment_id)


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
