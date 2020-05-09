from unittest import TestCase, main

from flask import json

from limbook_api import create_app

from tests.config import Config

"""Invalid token generated by unknown source for testing."""
example_invalid_token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ' \
                        '9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ikpv' \
                        'aG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwR' \
                        'JSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'

"""Valid token generated by Auth0 but has expired."""
example_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIs' \
                'ImtpZCI6IllhT3RnLWR4WmJMRmZOUnlOQkVEbSJ9.ey' \
                'Jpc3MiOiJodHRwczovL2xpbXZ1cy5hdXRoMC5jb20v' \
                'Iiwic3ViIjoiYXV0aDB8NWU5NTQyZmQ3ODNjNTAwYzB' \
                'lYzZiY2M5IiwiYXVkIjoiY29mZmVlLXNob3AtYXV0aCIs' \
                'ImlhdCI6MTU4NzM5NzM1NCwiZXhwIjoxNTg3NDA0NTU0L' \
                'CJhenAiOiJ4UzlBUnlldU1qYm5UbU1xMkJQVklab1BqN' \
                'lVjQzY2dyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiO' \
                'lsiZ2V0OmRyaW5rcy1kZXRhaWwiXX0.SWlxBTmsFFEcZ' \
                'tYXN-YqtRPBXLpjnMYfVYMVy_OXNoUHiTjBdcuIADEaX' \
                'dC6ZXzz5M9o7OIA4SKpSudv7P2efpvb6hW1DPp0UBcjG' \
                'se-hmO5fY0ZRcuvKyL-_srMyBdmacoKKXH55rxZ6mOi4' \
                'RcF8tQgcEhQzaL_KzD9UFPhKT3fTX_FFzALyg4G4WVBP' \
                'LiVAKpiIxuWuogDhjlDpk990j1xndxVQFI6J9m-JqSlZ' \
                'kdg6pSCiz2watWpOw4CnV28udvVx9ZiG5Uhp8Z9fiG2FP' \
                '3EheNdGNKdMCmTEe2ZF93QoYH5BvVsGdcFYYna-w-1TO' \
                '6QqrOUxHSZh0BBcNfekQ'

""" Valid token generated by Auth0 for user with role Barista.

This token has expired but can be used to check permissions by
bypassing token verification while testing.
"""
barista_token = example_token

""" Valid token generated by Auth0 for user with role Manager.

This token has expired but can be used to check permissions by
bypassing token verification while testing.
"""
manager_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IllhT' \
                '3RnLWR4WmJMRmZOUnlOQkVEbSJ9.eyJpc3MiOiJodHRwczovL2xpbXZ1c' \
                'y5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU5NTQyYWExOGJlMjQwYz' \
                'IyNTRiM2VkIiwiYXVkIjoiY29mZmVlLXNob3AtYXV0aCIsImlhdCI6MT' \
                'U4NzQ4NjgzMCwiZXhwIjoxNTg3NDk0MDMwLCJhenAiOiJ4UzlBUnlldU' \
                '1qYm5UbU1xMkJQVklab1BqNlVjQzY2dyIsInNjb3BlIjoiIiwicGVybW' \
                'lzc2lvbnMiOlsiZGVsZXRlOmRyaW5rcyIsImdldDpkcmlua3MtZGV0YW' \
                'lsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.XPX1f_JbJI' \
                'eL_a1G4eh1xXGehI-5LjaYSESphVSdtlfeBnOJCspzW5Q3s7KJswRZxu' \
                'hVT09trYurBQfeG7M1JemcGqHaub7o6a39GPGFLgxERr5EoknphpjjW1' \
                'KLhhQWkWfkCSwHhtFFeKY9EhqPVbX1X1NjAeU4CFaGVbCLP8UctgzVqT' \
                'dEGtPhdxvDpMdWYkP4mIldImU144X949q_BFqbm9XBdOXLxkCltS4RJW' \
                'mmO0W0qbCFHWXAz772FTl2IEN19GZawoX30h5VqDahlz-LJl1rEuTprc' \
                'PALuAqf54HFIjqlBouvQQUpNkjBzgIJJo4zD-YzsPHhs_3dP9RUg'

""" Valid token generated by Auth0 for user without any assigned role.

This token has expired but can be used to check invalid permissions by
bypassing token verification while testing.
"""
no_permission_token = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZC' \
                      'I6IllhT3RnLWR4WmJMRmZOUnlOQkVEbSJ9.eyJpc3MiOiJodHR' \
                      'wczovL2xpbXZ1cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8N' \
                      'WU5ZjFmZmY2YWZhY2IwY2JiMTBiYTJjIiwiYXVkIjoiY29mZmV' \
                      'lLXNob3AtYXV0aCIsImlhdCI6MTU4NzQ4NjcyNCwiZXhwIjox' \
                      'NTg3NDkzOTI0LCJhenAiOiJ4UzlBUnlldU1qYm5UbU1xMkJQVk' \
                      'lab1BqNlVjQzY2dyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnM' \
                      'iOltdfQ.IGGCeX9-O3P2B4_VYC_OIWacJO5jnW5XLFilHN7DV' \
                      '8h0nElD6ah0dSxnHse1FkO4G2iNV8S3kXuR5dlX95Um9ncfzG' \
                      'IpJF9rf9tQTbW6ODRFHh6s-r2Zr8mvVwoTyfVYj2szyTpxbBk' \
                      '9P4LkRAJNlTRA74xfe1jnUfDnlQGODaa2tPCrkH5tavrNN-om' \
                      'QJjeR-UIjnUseOg-TGdNL5keCsz5tCxbon1MLT1WSSqx_YtCR' \
                      'BZHkZc-H0KU5Fz9WwWEfLolCE7taLeLgTlDNCjotf6iib2zNfGX' \
                      '8d_vp4yN7QD4r4esk0khk1j2Hl4BVuq9XZr8FSM0yUP88_ZhQ28iMw'


class AuthTestCase(TestCase):
    """This class represents the trivia test case"""

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
        res = self.client().get('/secure-route?mock_jwt_claim=False')

        # assert
        self.assertEqual(res.status_code, 401)

    def test_cannot_access_protected_route_with_invalid_token(self):
        # given
        headers = {'Authorization': example_invalid_token}

        # make request
        # we are passing "mock_jwt_claim=False" as query to make the api
        # perform its normal behaviour. If it's not passed, by default
        # the api will bypass the expensive token verification call
        # to Auth0 for testing purpose.
        res = self.client().get(
            '/secure-route?mock_jwt_claim=False',
            headers=headers
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'invalid_header')

    def test_cannot_access_protected_route_with_expired_token(self):
        # given
        headers = {'Authorization': example_token}

        # make request
        # we are passing "mock_jwt_claim=False" as query to make the api
        # perform its normal behaviour. If it's not passed, by default
        # the api will bypass the expensive token verification call
        # to Auth0 for testing purpose.
        res = self.client().get(
            '/secure-route?mock_jwt_claim=False',
            headers=headers
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'token_expired')

    def test_cannot_access_protected_route_without_correct_permission(self):
        # given
        headers = {'Authorization': no_permission_token}

        # request
        res = self.client().get('/secure-route?mock_jwt_claim=True', headers=headers)
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
