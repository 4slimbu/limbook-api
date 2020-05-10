from unittest import TestCase, main

from flask import json

from limbook_api import create_app
from limbook_api.config_test import Config
from limbook_api.models.comment import create_random_comment
from limbook_api.models.post import create_random_post
from limbook_api.models.setup import db_drop_and_create_all

test_user_id = "auth0|5eb66a2d1cc1ac0c1496c16f"


class CommentsTestCase(TestCase):
    """This class represents the test case for Comments"""

    def setUp(self):
        """Define test variables and initialize app."""
        app = create_app(Config)
        app.testing = True
        client = app.test_client
        self.app = app
        self.client = client
        # refresh database
        db_drop_and_create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Comments Tests ----------------------------------------
    def test_cannot_access_comment_routes_without_correct_permission(self):
        # given
        headers = {'Authorization': self.app.config.get('NO_PERMISSION_TOKEN')}

        # make request
        # bypass actual token verification as we are interested in permission
        # part only

        # get comments
        res1 = self.client().get(
            '/posts/1/comments?mock_jwt_claim=True',
            headers=headers
        )
        data1 = json.loads(res1.data)

        # create comment
        res2 = self.client().post(
            '/posts/1/comments?mock_jwt_claim=True',
            headers=headers
        )
        data2 = json.loads(res2.data)

        # update comment
        res3 = self.client().patch(
            '/posts/1/comments/1?mock_jwt_claim=True',
            headers=headers
        )
        data3 = json.loads(res3.data)

        # delete comment
        res4 = self.client().delete(
            '/posts/1/comments/1?mock_jwt_claim=True',
            headers=headers
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
        post = create_random_post()
        comment = create_random_comment({
            "content": "New comment",
            "user_id": test_user_id,
            "post_id": post.id
        })
        headers = {'Authorization': self.app.config.get('EXAMPLE_TOKEN')}

        # make request
        res = self.client().get(
            '/posts/' + str(post.id) + '/comments?mock_jwt_claim=True',
            headers=headers
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('comments')[0], comment.format())

    def test_can_create_comments(self):
        # given
        headers = {'Authorization': self.app.config.get('EXAMPLE_TOKEN')}
        post = create_random_post()
        post_id = post.id
        comment = {"content": "My new Comment"}

        # make request
        res = self.client().post(
            '/posts/' + str(post.id) + '/comments?mock_jwt_claim=True',
            headers=headers,
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
        headers = {'Authorization': self.app.config.get('EXAMPLE_TOKEN')}
        post = create_random_post()
        comment = create_random_comment({
            "content": "My new comment",
            "user_id": test_user_id,
            "post_id": post.id
        })
        updated_comment_content = {
            "content": "My Updated Content"
        }

        # make request
        res = self.client().patch(
            '/posts/' + str(post.id) + '/comments/' + str(comment.id) + '?mock_jwt_claim=True',
            headers=headers,
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
        headers = {'Authorization': self.app.config.get('EXAMPLE_TOKEN')}
        post = create_random_post()
        comment = create_random_comment({
            'content': 'My new comment',
            'user_id': test_user_id,
            'post_id': post.id
        })

        # make request
        res = self.client().delete(
            '/posts/' + str(post.id) + '/comments/' + str(comment.id) + '?mock_jwt_claim=True',
            headers=headers
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('deleted_comment'), comment.format())


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
