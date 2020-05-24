from unittest import main

from flask import json

from tests.base import BaseTestCase, api_base


class StatsTestCase(BaseTestCase):
    """This class represents the test case for Stats"""

    # Auth Tests ----------------------------------------
    def test_can_access_stats_without_correct_permission(self):
        # make request
        res = self.client().get(
            api_base + '/stats'
            + '?mock_token_verification=True&permission='
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_can_access_stats(self):
        # request
        res = self.client().get(
            api_base
            + '/stats?mock_token_verification=True'
            + '&permission=read:stats'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('stats'))


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
