from unittest import main

from flask import json

from config_test import TestConfig
from limbook_api.v1.activities import generate_activity
from limbook_api.v1.posts import generate_post
from tests.base import BaseTestCase, test_user_id, api_base


class ActivitiesTestCase(BaseTestCase):
    """This class represents the test case for Activities"""

    # Activities Tests ----------------------------------------
    def test_cannot_access_activity_routes_without_correct_permission(self):
        # get activities
        res = self.client().get(
            api_base
            + '/activities?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # delete activity
        res = self.client().delete(
            api_base
            + '/activities/1?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_can_get_activities(self):
        # given
        post = generate_post()
        activity = generate_activity(
            user_id=test_user_id,
            post_id=post.id
        )

        # make request
        res = self.client().get(
            api_base
            + '/activities'
            + '?mock_token_verification=True&permission=read:activities'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('activities')[0], activity.format())

    def test_return_paginated_activities(self):
        # given
        for i in range(0, 30):
            generate_activity(user_id=test_user_id)

        # make request
        res = self.client().get(
            api_base
            + '/activities'
            + '?mock_token_verification=True&permission=read:activities'
            + '&page=2'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('activities')), TestConfig.PAGINATION)
        self.assertEqual(len(data.get('query_args')), 3)
        self.assertEqual(data.get('total'), 30)

    def test_can_delete_activities(self):
        # given
        post = generate_post()
        activity = generate_activity(
            user_id=test_user_id,
            post_id=post.id
        )

        # make request
        res = self.client().delete(
            api_base
            + '/activities/' + str(activity.id)
            + '?mock_token_verification=True&permission=delete:activities'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('deleted_id'), activity.id)


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
