from unittest import main

from flask import json

from limbook_api.v1.comments import generate_comment
from limbook_api.v1.posts import generate_post
from tests.base import BaseTestCase, test_user_id, api_base, pagination_limit


class CommentsTestCase(BaseTestCase):
    """This class represents the test case for Comments"""

    # Get Comments Tests ----------------------------------------
    def test_cannot_get_comments_without_correct_permission(self):
        # get comments
        res = self.client().get(
            api_base
            + '/comments?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_get_comments(self):
        # given
        post = generate_post()
        for i in range(0, 25):
            generate_comment(
                user_id=test_user_id,
                post_id=post.id
            )

        # make request
        res = self.client().get(
            api_base
            + '/comments'
            + '?mock_token_verification=True&permission=read:comments'
            + '&page=2'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('comments')), pagination_limit)
        self.assertEqual(data.get('total'), 25)
        self.assertEqual(len(data.get('query_args')), 3)

    # Get Comment Tests ----------------------------------------
    def test_cannot_get_comment_without_correct_permission(self):
        # get comments
        res = self.client().get(
            api_base
            + '/comments/1?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_get_comment(self):
        # given
        post = generate_post()
        generate_comment(
            user_id=test_user_id,
            post_id=post.id
        )

        # make request
        res = self.client().get(
            api_base
            + '/comments/1'
            + '?mock_token_verification=True&permission=read:comments'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('comment').get('id'), 1)

    # Create Comment Tests ----------------------------------------
    def test_cannot_create_comment_without_correct_permission(self):
        # create comment
        res = self.client().post(
            api_base
            + '/comments?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_can_create_comments(self):
        # given
        post = generate_post()
        post_id = post.id
        comment = {
            "post_id": post_id,
            "content": "My new Comment"
        }

        # make request
        res = self.client().post(
            api_base
            + '/comments'
            + '?mock_token_verification=True&permission=create:comments',
            json=comment
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            data.get('comment').get('content'), comment.get('content'))
        self.assertEqual(
            data.get('comment').get('user_id'), test_user_id)
        self.assertEqual(
            data.get('comment').get('post_id'), post_id)

    def test_cannot_reply_comment_without_correct_permission(self):
        # reply comment
        res = self.client().post(
            api_base
            + '/comments/1/replies?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

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
        self.assertTrue(expected_reply.items() <= data.get('comment').items())

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
            + '/comments/' + str(comment_id) + '/replies'
            + '?mock_token_verification=True&permission=create:comments',
            json=reply
        )
        data = json.loads(res.data)

        # assert
        self.assertTrue(data.get('comment').get('parent_id') == comment_id)

        # reply to reply
        res = self.client().post(
            api_base
            + '/comments/' + str(data.get('comment').get('id')) + '/replies'
            + '?mock_token_verification=True&permission=create:comments',
            json=reply
        )
        data = json.loads(res.data)

        # assert
        self.assertTrue(data.get('comment').get('parent_id') == comment_id)

        # reply to reply of reply
        res = self.client().post(
            api_base
            + '/comments/' + str(data.get('comment').get('id')) + '/replies'
            + '?mock_token_verification=True&permission=create:comments',
            json=reply
        )
        data = json.loads(res.data)

        # assert
        self.assertTrue(data.get('comment').get('parent_id') == comment_id)

    # Update Comment Tests ----------------------------------------
    def test_cannot_update_comment_without_correct_permission(self):
        # update comment
        res = self.client().patch(
            api_base
            + '/comments/1?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_cannot_update_others_comment(self):
        # given
        post = generate_post()
        comment = generate_comment(
            post_id=post.id
        )
        updated_comment_content = {
            "content": "My Updated Content"
        }

        # make request
        res = self.client().patch(
            api_base
            + '/comments/' + str(comment.id)
            + '?mock_token_verification=True&permission=update:comments',
            json=updated_comment_content
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data.get('error_code'), 'forbidden')

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
            + '/comments/' + str(comment.id)
            + '?mock_token_verification=True&permission=update:comments',
            json=updated_comment_content
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            data.get('comment').get('content'),
            updated_comment_content.get('content')
        )

    # Delete Comment Tests ----------------------------------------
    def test_cannot_delete_comment_without_correct_permission(self):
        # delete comment
        res = self.client().delete(
            api_base
            + '/comments/1?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_cannot_delete_others_comment(self):
        # given
        post = generate_post()
        comment = generate_comment(
            post_id=post.id
        )

        # make request
        res = self.client().delete(
            api_base
            + '/comments/' + str(comment.id)
            + '?mock_token_verification=True&permission=delete:comments'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 403)

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
            + '/comments/' + str(comment.id)
            + '?mock_token_verification=True&permission=delete:comments'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('deleted_id'), comment.id)


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
