import secrets
from datetime import datetime, timedelta
from unittest import main

from flask import json

from limbook_api.v1.permissions import generate_permission
from limbook_api.v1.users import generate_user, generate_role, User
from tests.base import BaseTestCase, api_base, get_access_token, \
    login_random_user, header_with_token, assert_successful_login


class UserTestCase(BaseTestCase):
    """This class represents the test case for Users"""

    # Auth Token and Permission Tests -----------------------------

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
        headers = header_with_token(self.app.config.get('EXAMPLE_INVALID_TOKEN'))

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
        headers = header_with_token(self.app.config.get('EXPIRED_TOKEN'))

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
        """ Test if permission filter works

        This is the only test where we are generating actual token.
        For other cases we are mocking the token generation, as
        the process is expensive and slows down the test
        """
        # request
        permission = generate_permission(slug='read:secure_route')
        token = get_access_token(self, permissions=[permission])
        headers = {'Authorization': 'Bearer ' + token}
        res = self.client().get(
            api_base + '/secure-route',
            headers=headers
        )

        # assert
        self.assertEqual(res.status_code, 200)

    def test_unverified_user_cannot_access_secure_routes(self):
        # login random user and get tokens
        res = login_random_user(self, is_verified=False)
        data = json.loads(res.data)
        access_token = data.get('access_token')

        # make request
        res = self.client().get(
            api_base + '/profile',
            headers=header_with_token(access_token)
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'user_not_verified')

    # Auth User Tests ----------------------------------------------

    def test_user_can_register(self):
        # request
        generate_role(
            name="Unverified User Role",
            slug="unverified_user",
            permissions=[]
        )
        user = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "johndoe@gmail.com",
            "phone_number": "9982938838",
            "password": "password",
            "confirm_password": "password"
        }

        res = self.client().post(
            api_base + '/register',
            json=user
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))
        self.assertTrue(data.get('user'))

    def test_user_can_send_verification_email(self):
        # given
        user = generate_user()

        # request
        res = self.client().post(
            api_base + '/send-verification-email',
            json={"email": user.email}
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))

    def test_user_can_verify_email(self):
        # given
        user = generate_user(
            email_verif_code=secrets.token_hex(8),
            email_verif_code_expires_on=datetime.now() + timedelta(hours=1)
        )

        # request
        res = self.client().post(
            api_base + '/verify-email',
            json={"verification_code": user.email_verif_code}
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))

    def test_user_can_send_reset_password_email(self):
        # given
        user = generate_user()

        # request
        res = self.client().post(
            api_base + '/send-reset-password-email',
            json={"email": user.email}
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))

    def test_user_can_reset_password(self):
        # Reset password -----------------------------------------
        # given
        user = generate_user(
            password_reset_code=secrets.token_hex(8),
            password_reset_code_expires_on=datetime.now() + timedelta(hours=1)
        )
        data = {
            "email": user.email,
            "password_reset_code": user.password_reset_code,
            "password": "new_password",
            "confirm_password": "new_password"
        }

        res = self.client().post(
            api_base + '/reset-password',
            json=data
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))

        # Assert login with new password ---------------------------
        user = User.query.first()
        login_data = {
            "email": user.email,
            "password": "new_password",
        }

        res = self.client().post(
            api_base + '/login',
            json=login_data
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('success'))
        self.assertTrue(data.get('access_token'))
        self.assertTrue(data.get('refresh_token'))

    def test_user_can_login(self):
        res = login_random_user(self)
        assert_successful_login(self, res)

    def test_user_can_refresh_access_token(self):
        # login random user and get tokens
        res = login_random_user(self)
        data = json.loads(res.data)
        refresh_token = data.get('refresh_token')

        # given
        headers = {'Authorization': 'Bearer ' + refresh_token}

        # make request
        res = self.client().get(
            api_base
            + '/refresh-token',
            headers=headers
        )

        # assert
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('access_token'))
        self.assertTrue(data.get('refresh_token'))
        self.assertNotEqual(data.get('refresh_token'), refresh_token)

    def test_user_can_logout(self):
        # login random user and get tokens
        res = login_random_user(self)
        data = json.loads(res.data)
        access_token = data.get('access_token')
        refresh_token = data.get('refresh_token')

        # make request
        res = self.client().post(
            api_base
            + '/logout',
            json={
                "refresh_token": refresh_token
            },
            headers=header_with_token(access_token)
        )

        # assert
        self.assertEqual(res.status_code, 200)

        # make request after logout using the previous access token
        res = self.client().post(
            api_base
            + '/logout',
            headers=header_with_token(access_token)
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'token_blacklisted')

        # make request after logout using the previous refresh token
        res = self.client().post(
            api_base
            + '/logout',
            headers=header_with_token(refresh_token)
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'token_blacklisted')


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
