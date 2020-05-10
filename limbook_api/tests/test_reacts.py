from unittest import main

from flask import json

from limbook_api.models.post import create_post
from limbook_api.tests.base import BaseTestCase


class ReactsTestCase(BaseTestCase):
    """This class represents the test case for Reacts"""

    # Reacts Tests ----------------------------------------
    def test_cannot_access_react_routes_without_correct_permission(self):
        # get reacts
        res1 = self.client().get(
            '/posts/1/reacts'
            + '?mock_token_verification=True'
        )
        data1 = json.loads(res1.data)

        # toggle react
        res2 = self.client().post(
            '/posts/1/reacts/toggle'
            + '?mock_token_verification=True'
        )
        data2 = json.loads(res2.data)

        # assert
        self.assertEqual(res1.status_code, 401)
        self.assertEqual(data1.get('error_code'), 'no_permission')
        self.assertEqual(res2.status_code, 401)
        self.assertEqual(data2.get('error_code'), 'no_permission')

    def test_can_toggle_reacts(self):
        # given
        post = create_post()
        post_id = post.id

        # make request
        res = self.client().post(
            '/posts/' + str(post_id) + '/reacts/toggle'
            + '?mock_token_verification=True&permission=update:reacts'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('reacts')), 1)
        self.assertEqual(data.get('reacts_count'), 1)

        # make request
        res = self.client().post(
            '/posts/' + str(post_id) + '/reacts/toggle'
            + '?mock_token_verification=True&permission=update:reacts'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('reacts')), 0)
        self.assertEqual(data.get('reacts_count'), 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
