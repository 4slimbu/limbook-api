from unittest import main

from flask import json

from limbook_api.v1.friends import generate_friend
from limbook_api.v1.posts import generate_post
from limbook_api.v1.users import generate_user, User
from tests.base import BaseTestCase, api_base, header_with_token, \
    login_random_user, pagination_limit


class PersonalTestCase(BaseTestCase):
    """This class represents the test case for Personal routes"""

    def test_unverified_user_cannot_access_personal_routes(self):
        # get profile
        res = self.client().get(
            api_base + '/profile'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'unauthorized')

        # update profile
        res = self.client().patch(
            api_base + '/profile'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'unauthorized')

        # get news-feed
        res = self.client().get(
            api_base + '/news-feed'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'unauthorized')

        # get timeline
        res = self.client().get(
            api_base + '/timeline'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'unauthorized')

    def test_user_can_see_profile(self):
        # login random user and get tokens
        res = login_random_user(self, is_verified=True)
        data = json.loads(res.data)
        access_token = data.get('access_token')

        # make request
        res = self.client().get(
            api_base + '/profile',
            headers=header_with_token(access_token)
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('user'))

    def test_user_can_update_profile(self):
        # login random user and get tokens
        res = login_random_user(self, is_verified=True)
        data = json.loads(res.data)
        access_token = data.get('access_token')
        update = {
            "first_name": "Updated first name",
            "last_name": "Updated last_name",
            "profile_picture": "updated.jpg",
            "cover_picture": "updated.jpg",
        }

        # make request
        res = self.client().patch(
            api_base + '/profile',
            headers=header_with_token(access_token),
            json=update
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('user').items() >= update.items())
        user_in_db = User.query.filter(User.id == 1).first()
        self.assertEqual(user_in_db.first_name, update['first_name'])
        self.assertEqual(user_in_db.last_name, update['last_name'])
        self.assertEqual(user_in_db.profile_picture, update['profile_picture'])
        self.assertEqual(user_in_db.cover_picture, update['cover_picture'])

    def test_user_can_see_timeline(self):
        # create posts
        for i in range(0, 15):
            generate_post(user_id=1)

        for i in range(0, 5):
            generate_post(user_id=2)

        # make request
        res = self.client().get(
            api_base + '/timeline'
            + '?mock_token_verification=True&permission='
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('posts'))
        self.assertEqual(len(data.get('posts')), pagination_limit)
        self.assertEqual(data.get('total'), 15)

    def test_user_can_see_news_feed(self):
        """ News feed should show posts by user and friends

        Here we are generating 3 users, 1 and 2 are friends. So,
        news-feed should display posts by 1 and 2 only.
        """
        generate_user()
        generate_user()
        generate_user()
        generate_friend(requester_id=1, receiver_id=2, is_friend=True)

        for i in range(0, 10):
            generate_post(user_id=1)

        for i in range(0, 5):
            generate_post(user_id=2)

        for i in range(0, 5):
            generate_post(user_id=3)

        # make request
        res = self.client().get(
            api_base + '/news-feed'
            + '?mock_token_verification=True&permission='
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('posts'))
        self.assertEqual(len(data.get('posts')), pagination_limit)
        self.assertEqual(data.get('total'), 15)


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
