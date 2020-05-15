from unittest import main

from limbook_api.tests.base import BaseTestCase


class AppTestCase(BaseTestCase):
    """This class represents the test case for Authentication"""

    # App runs ----------------------------------------
    def test_app_is_running(self):
        # make request
        res = self.client().get('/')

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue("Welcome to Limbook Api" in res.get_data(as_text=True))


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
