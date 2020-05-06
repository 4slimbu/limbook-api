from unittest import TestCase, main

from limbook_api import create_app


class LimbookApiTestCase(TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        app = create_app()
        app.testing = True
        client = app.test_client
        self.app = app
        self.client = client

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Auth Tests ----------------------------------------
    def test_get_home(self):
        # make request
        res = self.client().get('/')

        # assert
        self.assertIn('Limbook api', res.data.decode('utf-8'))


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
