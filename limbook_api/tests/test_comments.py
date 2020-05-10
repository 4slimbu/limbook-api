from unittest import main

from flask import json

from limbook_api.models.comment import create_comment
from limbook_api.models.post import create_post
from limbook_api.tests.base import BaseTestCase, test_user_id


class CommentsTestCase(BaseTestCase):
    """This class represents the test case for Comments"""

    # Comments Tests ----------------------------------------
    def test_cannot_access_comment_routes_without_correct_permission(self):
        # get comments
        res1 = self.client().get(
            '/posts/1/comments?mock_token_verification=True'
        )
        data1 = json.loads(res1.data)

        # create comment
        res2 = self.client().post(
            '/posts/1/comments?mock_token_verification=True'
        )
        data2 = json.loads(res2.data)

        # update comment
        res3 = self.client().patch(
            '/posts/1/comments/1?mock_token_verification=True'
        )
        data3 = json.loads(res3.data)

        # delete comment
        res4 = self.client().delete(
            '/posts/1/comments/1?mock_token_verification=True'
        )
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

    def test_can_get_comments(self):
        # given
        post = create_post()
        comment = create_comment({
            "content": "New comment",
            "user_id": test_user_id,
            "post_id": post.id
        })

        # make request
        res = self.client().get(
            '/posts/' + str(post.id) + '/comments'
            + '?mock_token_verification=True&permission=read:comments'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('comments')[0], comment.format())

    def test_can_create_comments(self):
        # given
        post = create_post()
        post_id = post.id
        comment = {"content": "My new Comment"}

        # make request
        res = self.client().post(
            '/posts/' + str(post.id) + '/comments'
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
        post = create_post()
        comment = create_comment({
            "content": "My new comment",
            "user_id": test_user_id,
            "post_id": post.id
        })
        updated_comment_content = {
            "content": "My Updated Content"
        }

        # make request
        res = self.client().patch(
            '/posts/' + str(post.id) + '/comments/' + str(comment.id)
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
        post = create_post()
        comment = create_comment({
            'content': 'My new comment',
            'user_id': test_user_id,
            'post_id': post.id
        })

        # make request
        res = self.client().delete(
            '/posts/' + str(post.id) + '/comments/' + str(comment.id)
            + '?mock_token_verification=True&permission=delete:comments'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('deleted_comment'), comment.format())


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
