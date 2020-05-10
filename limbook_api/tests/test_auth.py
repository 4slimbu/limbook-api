from unittest import TestCase, main

from flask import json

from limbook_api import create_app
from limbook_api.config_test import Config


class AuthTestCase(TestCase):
    """This class represents the test case for Authenticaiton"""

    def setUp(self):
        """Define test variables and initialize app."""
        app = create_app(Config)
        app.testing = True
        client = app.test_client
        self.app = app
        self.client = client

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Auth Tests ----------------------------------------
    def test_can_access_public_route_without_token(self):
        # make request
        res = self.client().get('/')

        # assert
        self.assertEqual(res.status_code, 200)

    def test_cannot_access_protected_route_without_token(self):
        # make request
        # we are passing "mock_jwt_claim=False" as query to make the api
        # perform its normal behaviour. If it's not passed, by default
        # the api will bypass the expensive token verification call
        # to Auth0 for testing purpose.
        res = self.client().get('/secure-route')

        # assert
        self.assertEqual(res.status_code, 401)

    def test_cannot_access_protected_route_with_invalid_token(self):
        # given
        headers = {'Authorization': self.app.config.get('EXAMPLE_INVALID_TOKEN')}

        # make request
        # we are passing "mock_jwt_claim=False" as query to make the api
        # perform its normal behaviour. If it's not passed, by default
        # the api will bypass the expensive token verification call
        # to Auth0 for testing purpose.
        res = self.client().get(
            '/secure-route',
            headers=headers
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'invalid_header')

    def test_cannot_access_protected_route_with_expired_token(self):
        # given
        headers = {'Authorization': self.app.config.get('EXAMPLE_TOKEN')}

        # make request
        res = self.client().get(
            '/secure-route',
            headers=headers
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'token_expired')

    def test_cannot_access_protected_route_without_correct_permission(self):
        # given
        headers = {'Authorization': self.app.config.get('NO_PERMISSION_TOKEN')}

        # request
        # we are passing "mock_jwt_claim=True" to bypass the
        # token verification as we are interested in testing permission only
        res = self.client().get('/secure-route?mock_jwt_claim=True', headers=headers)
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_can_access_protected_route_with_correct_permission(self):
        # given
        headers = {'Authorization': self.app.config.get('EXAMPLE_TOKEN')}

        # request
        # we are passing "mock_jwt_claim=True" to bypass the
        # token verification as we are interested in testing permission only
        res = self.client().get('/secure-route?mock_jwt_claim=True',
                                headers=headers)

        # assert
        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
