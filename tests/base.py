import os
import shutil
from unittest import TestCase

from config_test import TestConfig
from limbook_api import create_app
from limbook_api.db import db_drop_and_create_all

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
