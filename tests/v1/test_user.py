from unittest import main

from flask import json

from limbook_api.v1.roles import generate_role
from limbook_api.v1.users import generate_user, User
from tests.base import BaseTestCase, api_base


class UsersTestCase(BaseTestCase):
    """This class represents the test case for Users"""

    # Users Tests ----------------------------------------
    def test_cannot_access_user_routes_without_correct_permission(self):
        # get users
        res = self.client().get(
            api_base
            + '/users?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # create user
        res = self.client().post(
            api_base
            + '/users?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # update user
        res = self.client().patch(
            api_base
            + '/users/1?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # delete user
        res = self.client().delete(
            api_base
            + '/users/1?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_can_get_users(self):
        # given
        generate_user()

        # make request
        res = self.client().get(
            api_base
            + '/users'
            + '?mock_token_verification=True&permission=read:users'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('users')), 1)

    def test_user_pagination(self):
        # given
        for i in range(0, 3):
            generate_user()

        # make request
        res = self.client().get(
            api_base
            + '/users'
            + '?mock_token_verification=True&permission=read:users&per_page=2'
            + '&page=1'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('users')), 2)
        self.assertEqual(data.get('total'), 3)
        self.assertEqual(len(data.get('query_args')), 4)

    def test_can_create_users(self):
        # given
        role = generate_role()
        user = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@gmail.com",
            "phone_number": "9982938838",
            "password": "password",
            "confirm_password": "password",
            "role_id": role.id,
            "profile_picture": "http://dummyimages.com/200/200",
            "cover_picture": "http://dummyimages.com/1000/500"
        }

        # make request
        res = self.client().post(
            api_base
            + '/users'
            + '?mock_token_verification=True&permission=create:users',
            json=user
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('user').get('email'), user.get('email'))
        self.assertTrue(User.query.count(), 1)

    def test_can_update_users(self):
        # given
        user = generate_user()
        updated_user_content = {
            "first_name": "Updated First Name"
        }

        # make request
        res = self.client().patch(
            api_base
            + '/users/' + str(user.id)
            + '?mock_token_verification=True&permission=update:users',
            json=updated_user_content
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            data.get('user').get('first_name'),
            updated_user_content.get('first_name')
        )

    def test_can_delete_users(self):
        # given
        user = generate_user()

        # make request
        res = self.client().delete(
            api_base
            + '/users/' + str(user.id)
            + '?mock_token_verification=True&permission=delete:users'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('deleted_id'), user.id)

    # User-role-permission tests ---------------------------
    def test_can_assign_role_to_user(self):
        # given
        role = generate_role()
        user = generate_user()
        update_data = {
            "role_id": role.id
        }

        # make request
        res = self.client().patch(
            api_base
            + '/users/' + str(user.id)
            + '?mock_token_verification=True&permission=update:users',
            json=update_data
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            data.get('user').get('role_id'),
            update_data.get('role_id')
        )


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
