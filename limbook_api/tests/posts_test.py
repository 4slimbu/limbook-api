from unittest import TestCase, main

from flask import json

from limbook_api import create_app
from limbook_api.config_test import Config
from limbook_api.db.main import create_random_post, db_drop_and_create_all


class PostsTestCase(TestCase):
    """This class represents the test case for Posts"""

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

    # Posts Tests ----------------------------------------
    def test_cannot_access_post_routes_without_correct_permission(self):
        # given
        headers = {'Authorization': self.app.config.get('NO_PERMISSION_TOKEN')}

        # make request
        # bypass actual token verification as we are interested in permission
        # part only
        res1 = self.client().get('/posts?mock_jwt_claim=True', headers=headers)
        data1 = json.loads(res1.data)
        res2 = self.client().post('/posts?mock_jwt_claim=True', headers=headers)
        data2 = json.loads(res2.data)

        # assert
        self.assertEqual(res1.status_code, 401)
        self.assertEqual(data1.get('error_code'), 'no_permission')
        self.assertEqual(res2.status_code, 401)
        self.assertEqual(data2.get('error_code'), 'no_permission')

    def test_can_get_posts(self):
        # given
        post = create_random_post()
        headers = {'Authorization': self.app.config.get('EXAMPLE_TOKEN')}

        # make request
        res = self.client().get('/posts?mock_jwt_claim=True', headers=headers)
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('posts')[0], post.format())

    def test_can_create_posts(self):
        # given
        headers = {'Authorization': self.app.config.get('EXAMPLE_TOKEN')}
        post = {
            "content": "My new Post"
        }

        # make request
        res = self.client().post(
            '/posts?mock_jwt_claim=True',
            headers=headers,
            json=post
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('posts')[0]['content'], post['content'])
        # id of user from token we are using: auth0|5eb66a2d1cc1ac0c1496c16f
        self.assertEqual(
            data.get('posts')[0]['user_id'],
            'auth0|5eb66a2d1cc1ac0c1496c16f'
        )

    def test_can_create_posts(self):
        # given
        headers = {'Authorization': self.app.config.get('EXAMPLE_TOKEN')}
        post = {
            "content": "My new Post"
        }

        # make request
        res = self.client().post(
            '/posts?mock_jwt_claim=True',
            headers=headers,
            json=post
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('posts')[0]['content'], post['content'])
        # id of user from token we are using: auth0|5eb66a2d1cc1ac0c1496c16f
        self.assertEqual(
            data.get('posts')[0]['user_id'],
            'auth0|5eb66a2d1cc1ac0c1496c16f'
        )


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
