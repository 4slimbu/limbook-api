from unittest import TestCase, main

from flask import json

from limbook_api import create_app
from limbook_api.config_test import Config
from limbook_api.db.main import create_random_post, db_drop_and_create_all


class PostsTestCase(TestCase):
    """This class represents the test case for Posts"""

    def setUp(self):
        """Define test variables and initialize app."""
        app = create_app(Config)
        app.testing = True
        client = app.test_client
        self.app = app
        self.client = client
        # refresh database
        db_drop_and_create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Posts Tests ----------------------------------------
    def test_can_get_posts(self):
        # given
        post = create_random_post()

        # make request
        res = self.client().get('/posts')
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('posts')[0], post.format())


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
