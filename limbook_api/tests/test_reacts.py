from unittest import TestCase, main

from flask import json

from limbook_api import create_app
from limbook_api.config_test import Config
from limbook_api.models.post import create_random_post
from limbook_api.models.setup import db_drop_and_create_all

test_user_id = "auth0|5eb66a2d1cc1ac0c1496c16f"


class ReactsTestCase(TestCase):
    """This class represents the test case for Reacts"""

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

    # Reacts Tests ----------------------------------------
    def test_cannot_access_react_routes_without_correct_permission(self):
        # given
        headers = {'Authorization': self.app.config.get('NO_PERMISSION_TOKEN')}

        # make request
        # bypass actual token verification as we are interested in permission
        # part only

        # get reacts
        res1 = self.client().get(
            '/posts/1/reacts?mock_jwt_claim=True',
            headers=headers
        )
        data1 = json.loads(res1.data)

        # toggle react
        res2 = self.client().post(
            '/posts/1/reacts/toggle?mock_jwt_claim=True',
            headers=headers
        )
        data2 = json.loads(res2.data)

        # assert
        self.assertEqual(res1.status_code, 401)
        self.assertEqual(data1.get('error_code'), 'no_permission')
        self.assertEqual(res2.status_code, 401)
        self.assertEqual(data2.get('error_code'), 'no_permission')

    def test_can_toggle_reacts(self):
        # given
        post = create_random_post()
        post_id = post.id
        headers = {'Authorization': self.app.config.get('EXAMPLE_TOKEN')}

        # make request
        res = self.client().post(
            '/posts/' + str(post_id) + '/reacts/toggle?mock_jwt_claim=True',
            headers=headers
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('reacts')), 1)
        self.assertEqual(data.get('reacts_count'), 1)

        # make request
        res = self.client().post(
            '/posts/' + str(post_id) + '/reacts/toggle?mock_jwt_claim=True',
            headers=headers
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('reacts')), 0)
        self.assertEqual(data.get('reacts_count'), 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
