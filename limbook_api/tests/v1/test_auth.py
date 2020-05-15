from unittest import main

from flask import json

from limbook_api.tests.base import BaseTestCase
from limbook_api.tests.v1 import api_base


class AuthTestCase(BaseTestCase):
    """This class represents the test case for Authentication"""

    # Auth Tests ----------------------------------------
    def test_cannot_access_protected_route_without_token(self):
        # make request
        res = self.client().get(
            api_base
            + '/secure-route'
        )

        # assert
        self.assertEqual(res.status_code, 401)

    def test_cannot_access_protected_route_with_invalid_token(self):
        # given
        headers = {'Authorization': self.app.config.get('EXAMPLE_INVALID_TOKEN')}

        # make request
        res = self.client().get(
            api_base
            + '/secure-route',
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
            api_base
            + '/secure-route',
            headers=headers
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'token_expired')

    def test_cannot_access_protected_route_without_correct_permission(self):
        # request
        res = self.client().get(
            api_base
            + '/secure-route?mock_token_verification=True&permission='
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_can_access_protected_route_with_correct_permission(self):
        # request
        res = self.client().get(
            api_base
            + '/secure-route'
            + '?mock_token_verification=True&permission=read:secure_route'
        )

        # assert
        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
