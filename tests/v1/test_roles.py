from unittest import main

from flask import json

from limbook_api.v1.permissions import generate_permission
from limbook_api.v1.roles import generate_role, Role
from tests.base import BaseTestCase, api_base


class RolesTestCase(BaseTestCase):
    """This class represents the test case for Roles"""

    # Roles Tests ----------------------------------------
    def test_cannot_access_role_routes_without_correct_permission(self):
        # get roles
        res = self.client().get(
            api_base
            + '/roles?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # create role
        res = self.client().post(
            api_base
            + '/roles?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # update role
        res = self.client().patch(
            api_base
            + '/roles/1?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # delete role
        res = self.client().delete(
            api_base
            + '/roles/1?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_can_get_roles(self):
        # given
        generate_role()

        # make request
        res = self.client().get(
            api_base
            + '/roles'
            + '?mock_token_verification=True&permission=read:roles'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('roles')), 1)

    def test_role_pagination(self):
        # given
        for i in range(0, 3):
            generate_role()

        # make request
        res = self.client().get(
            api_base
            + '/roles'
            + '?mock_token_verification=True&permission=read:roles&per_page=2'
            + '&page=1'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('roles')), 2)
        self.assertEqual(data.get('total'), 3)
        self.assertEqual(len(data.get('query_args')), 4)

    def test_can_create_roles(self):
        # given
        role = {
            "slug": "admin",
            "name": "Admin",
            "description": "Can manage everything",
        }

        # make request
        res = self.client().post(
            api_base
            + '/roles'
            + '?mock_token_verification=True&permission=create:roles',
            json=role
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('role').items() >= role.items())
        self.assertTrue(Role.query.count(), 1)

    def test_can_update_roles(self):
        # given
        role = generate_role()
        update = {
            "name": "Updated Role Name",
            "description": "Updated Description"
        }

        # make request
        res = self.client().patch(
            api_base
            + '/roles/' + str(role.id)
            + '?mock_token_verification=True&permission=update:roles',
            json=update
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('role').items() >= update.items())

    def test_can_delete_roles(self):
        # given
        role = generate_role()

        # make request
        res = self.client().delete(
            api_base
            + '/roles/' + str(role.id)
            + '?mock_token_verification=True&permission=delete:roles'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('deleted_id'), role.id)

    # Role-Permission Test ---------------------------------
    def test_cannot_access_role_permission_routes_without_permission(self):
        # add/update permissions of a role
        role = generate_role()
        res = self.client().post(
            api_base
            + '/roles/' + str(role.id) + '/permissions'
            + '?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_can_assign_permissions_to_role(self):
        # given
        role = generate_role()
        permission1 = generate_permission()
        permission2 = generate_permission()
        data = {
            "permission_ids": [permission1.id, permission2.id]
        }

        # make request
        res = self.client().post(
            api_base
            + '/roles/' + str(role.id) + '/permissions'
            + '?mock_token_verification=True&permission=create:roles',
            json=data
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('role').get('permissions')), 2)

        # Re-assign permissions
        permission3 = generate_permission()
        permission4 = generate_permission()
        data = {
            "permission_ids": [permission3.id, permission4.id]
        }

        # make request
        res = self.client().post(
            api_base
            + '/roles/' + str(role.id) + '/permissions'
            + '?mock_token_verification=True&permission=create:roles',
            json=data
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('role').get('permissions')), 2)
        self.assertEqual(
            data.get('role').get('permissions')[0].get('id'), permission3.id)
        self.assertEqual(
            data.get('role').get('permissions')[1].get('id'), permission4.id)

    def test_can_get_role_with_permissions(self):
        # given
        role = generate_role()

        # make request
        res = self.client().get(
            api_base
            + '/roles/' + str(role.id)
            + '?mock_token_verification=True&permission=read:roles'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data.get('role').get('permissions')) > -1)


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
