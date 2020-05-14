from unittest import main

from flask import json

from limbook_api.posts import generate_post
from limbook_api.tests.base import BaseTestCase


class ReactsTestCase(BaseTestCase):
    """This class represents the test case for Posts"""

    # Posts Tests ----------------------------------------
    def test_cannot_access_post_routes_without_correct_permission(self):
        # get reacts
        res = self.client().get(
            '/posts/1/reacts'
            + '?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # toggle react
        res = self.client().post(
            '/posts/1/reacts/toggle'
            + '?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_can_react_and_unreact_post(self):
        # given
        post = generate_post()
        post_id = post.id

        # make request
        res = self.client().post(
            '/posts/' + str(post_id) + '/reacts/toggle'
            + '?mock_token_verification=True&permission=update:reacts'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('post').get('reacts')), 1)

        # make request
        res = self.client().post(
            '/posts/' + str(post_id) + '/reacts/toggle'
            + '?mock_token_verification=True&permission=update:reacts'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('post').get('reacts')), 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
