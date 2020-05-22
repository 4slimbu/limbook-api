from unittest import main

from flask import json

from limbook_api.v1.permissions import generate_permission, Permission
from tests.base import BaseTestCase, api_base


class PermissionsTestCase(BaseTestCase):
    """This class represents the test case for Permissions"""

    # Permissions Tests ----------------------------------------
    def test_cannot_access_permission_routes_without_correct_permission(self):
        # get permissions
        res = self.client().get(
            api_base
            + '/permissions?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # create permission
        res = self.client().post(
            api_base
            + '/permissions?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # update permission
        res = self.client().patch(
            api_base
            + '/permissions/1?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # delete permission
        res = self.client().delete(
            api_base
            + '/permissions/1?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_can_get_permissions(self):
        # given
        generate_permission()

        # make request
        res = self.client().get(
            api_base
            + '/permissions'
            + '?mock_token_verification=True&permission=read:permissions'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('permissions')), 1)

    def test_permission_pagination(self):
        # given
        for i in range(0, 3):
            generate_permission()

        # make request
        res = self.client().get(
            api_base
            + '/permissions'
            + '?mock_token_verification=True&permission=read:permissions'
            + '&per_page=2'
            + '&page=1'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('permissions')), 2)
        self.assertEqual(data.get('total'), 3)
        self.assertEqual(len(data.get('query_args')), 4)

    def test_can_create_permissions(self):
        # given
        permission = {
            "slug": "read:users",
            "name": "Get Users",
            "description": "Can read users",
        }

        # make request
        res = self.client().post(
            api_base
            + '/permissions'
            + '?mock_token_verification=True&permission=create:permissions',
            json=permission
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('permission').items() >= permission.items())
        self.assertTrue(Permission.query.count(), 1)

    def test_can_update_permissions(self):
        # given
        permission = generate_permission()
        update = {
            "name": "Updated Permission Name",
            "description": "Updated Description"
        }

        # make request
        res = self.client().patch(
            api_base
            + '/permissions/' + str(permission.id)
            + '?mock_token_verification=True&permission=update:permissions',
            json=update
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('permission').items() >= update.items())

    def test_can_delete_permissions(self):
        # given
        permission = generate_permission()

        # make request
        res = self.client().delete(
            api_base
            + '/permissions/' + str(permission.id)
            + '?mock_token_verification=True&permission=delete:permissions'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('deleted_id'), permission.id)


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
