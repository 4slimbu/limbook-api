import os
import shutil
from unittest import TestCase

from flask import json

from limbook_api import create_app
from config_test import TestConfig
from limbook_api.db import db_drop_and_create_all
from limbook_api.v1.roles import generate_role
from limbook_api.v1.users import generate_user

test_user_id = 1
api_base = '/v1'
pagination_limit = TestConfig.PAGINATION


def mock_token_verification(permission=None):
    """ Mock payload with custom permission

        Parameters:
            permission (string): e.g: "read:posts,create:posts"

        returns:
            payload (dict)
    """
    if permission is None:
        permission = []
    else:
        permission = permission.split(',')

    return {
        'iat': 1589041232,
        'exp': 1589048432,
        'sub': 1,
        'is_verified': True,
        'permissions': permission
    }


def header_with_token(token):
    return {'Authorization': 'Bearer ' + token}


def get_access_token(self, permissions=None):
    permissions = permissions if permissions else []
    role = generate_role(permissions=permissions)
    user = generate_user(
        role_id=role.id,
        email_verified=True,
        password="password"
    )

    login_data = {
        "email": user.email,
        "password": "password",
    }

    res = self.client().post(
        api_base + '/login',
        json=login_data
    )

    return json.loads(res.data).get('access_token')


def login_random_user(self, is_verified=True):
    user = generate_user(password="password", email_verified=is_verified)
    login_data = {
        "email": user.email,
        "password": "password",
    }

    return self.client().post(
        api_base + '/login',
        json=login_data
    )


def assert_successful_login(self, res):
    data = json.loads(res.data)

    # assert
    self.assertEqual(res.status_code, 200)
    self.assertTrue(data.get('success'))
    self.assertTrue(data.get('access_token'))
    self.assertTrue(data.get('refresh_token'))


class BaseTestCase(TestCase):
    """This class represents the test case for Activities"""

    def setUp(self):
        """Define test variables and initialize app."""
        app = create_app(TestConfig)
        app.testing = True
        client = app.test_client
        self.app = app
        self.client = client
        # refresh database
        db_drop_and_create_all()

    def tearDown(self):
        """Executed after reach test"""
        # refresh image test dir
        test_img_dir = self.app.root_path + '/' + TestConfig.IMG_UPLOAD_DIR
        if os.path.isdir(test_img_dir):
            shutil.rmtree(self.app.root_path + '/' + TestConfig.IMG_UPLOAD_DIR)
