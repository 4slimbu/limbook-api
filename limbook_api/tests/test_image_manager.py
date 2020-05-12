import io
import os
from unittest import main

from flask import json

from limbook_api.image_manager import generate_img_in_bytes, create_image
from limbook_api.posts import create_post
from limbook_api.tests.base import BaseTestCase, test_user_id


class ImageManagerTestCase(BaseTestCase):
    """This class represents the test case for Image Manager"""

    def test_cannot_access_image_routes_without_correct_permission(self):
        # create image
        res1 = self.client().post(
            '/images'
            + '?mock_token_verification=True'
        )
        data1 = json.loads(res1.data)

        # get image
        res2 = self.client().get(
            '/images/1'
            + '?mock_token_verification=True'
        )
        data2 = json.loads(res2.data)

        # get images
        res3 = self.client().get(
            '/images'
            + '?mock_token_verification=True'
        )
        data3 = json.loads(res3.data)

        # delete image
        res4 = self.client().delete(
            '/images/1'
            + '?mock_token_verification=True'
        )
        data4 = json.loads(res4.data)

        # assert
        self.assertEqual(res1.status_code, 401)
        self.assertEqual(data1.get('error_code'), 'no_permission')
        self.assertEqual(res2.status_code, 401)
        self.assertEqual(data2.get('error_code'), 'no_permission')
        self.assertEqual(res3.status_code, 401)
        self.assertEqual(data3.get('error_code'), 'no_permission')
        self.assertEqual(res4.status_code, 401)
        self.assertEqual(data4.get('error_code'), 'no_permission')

    def test_cannot_retrieve_other_images(self):
        """ I can only retrieve my images """
        # given
        image = create_image()

        # make request
        res = self.client().get(
            '/images'
            + '?mock_token_verification=True&permission=read:images'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('images')), 0)
        self.assertEqual(data.get('images_count'), 0)

    def test_can_retrieve_own_images(self):
        """ I can retrieve all my images """
        # given
        image1 = create_image(user_id=test_user_id)
        image2 = create_image(user_id=test_user_id)
        image3 = create_image()
        image4 = create_image()

        # make request
        res = self.client().get(
            '/images'
            + '?mock_token_verification=True&permission=read:images'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('images')), 2)
        self.assertEqual(data.get('images_count'), 2)

    def test_cannot_upload_invalid_image(self):
        # given
        image = (io.BytesIO(b"invalid"), 'test.jpg')
        data = {"image": image}

        # make request
        res = self.client().post(
            '/images'
            + '?mock_token_verification=True&permission=create:images',
            data=data,
            content_type='multipart/form-data'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data.get('error_code'), 'image_upload_error')

    def test_cannot_upload_image_greater_than_1mb(self):
        # given
        image = (io.BytesIO(generate_img_in_bytes(9000, 9000)), 'test.jpg')
        data = {"image": image}

        # make request
        res = self.client().post(
            '/images'
            + '?mock_token_verification=True&permission=create:images',
            data=data,
            content_type='multipart/form-data'
        )

        # assert
        self.assertEqual(res.status_code, 413)

    def test_can_upload_jpg_jpeg_and_png_images_only(self):
        # given
        image = (io.BytesIO(generate_img_in_bytes()), 'test.gif')
        data = {"image": image}

        # make request
        res = self.client().post(
            '/images'
            + '?mock_token_verification=True&permission=create:images',
            data=data,
            content_type='multipart/form-data'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data.get('error_code'), 'file_extension_not_allowed')

    def test_can_create_image(self):
        # given
        image = (io.BytesIO(generate_img_in_bytes()), 'test.jpg')
        data = {"image": image}

        # make request
        res = self.client().post(
            '/images'
            + '?mock_token_verification=True&permission=create:images',
            data=data,
            content_type='multipart/form-data'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('image').get('user_id'), test_user_id)
        self.assertTrue(
            os.path.isfile(data.get('image').get('url').get('large')))
        self.assertTrue(
            os.path.isfile(data.get('image').get('url').get('medium')))
        self.assertTrue(
            os.path.isfile(data.get('image').get('url').get('thumb')))

    def test_cannot_retrieve_others_image_by_id(self):
        """ User should not be able to retrieve other images

        Here we are creating the image with random user_id
        but are using the test_user_id to authenticate
        so, user shouldn't be able to get the image
        """
        # given
        image = create_image()
        image_id = image.id

        # make request
        res = self.client().get(
            '/images/' + str(image_id)
            + '?mock_token_verification=True&permission=create:images'
        )

        # assert
        self.assertEqual(res.status_code, 401)

    def test_can_retrieve_own_image_by_id(self):
        """
        If I create the image, then I should be able to
        retrieve it.
        """
        # given
        image = create_image({
            'user_id': test_user_id,
            'url': json.dumps({
                "thumb": "thumb.jpg",
                "medium": "medium.jpg",
                "large": "large.jpg"
            })
        })

        # make request
        res = self.client().get(
            '/images/' + str(image.id)
            + '?mock_token_verification=True&permission=read:images'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(image.format(), data.get('image'))

    def test_cannot_delete_others_image(self):
        """
        I should not be able to delete image created by other user.
        """
        # given
        image = create_image()

        # make request
        res = self.client().delete(
            '/images/' + str(image.id)
            + '?mock_token_verification=True&permission=read:images'
        )

        # assert
        self.assertEqual(res.status_code, 401)

    def test_can_delete_own_image(self):
        """
        I should be able to delete my image
        """
        # given
        image = (io.BytesIO(generate_img_in_bytes()), 'test.jpg')
        data = {"image": image}

        # save image
        res = self.client().post(
            '/images'
            + '?mock_token_verification=True&permission=create:images',
            data=data
        )
        image = json.loads(res.data).get('image')

        # make delete request
        res = self.client().delete(
            '/images/' + str(image.get('id'))
            + '?mock_token_verification=True&permission=delete:images'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertEqual(data.get('deleted_image'), image)
        self.assertFalse(
            os.path.isfile(data.get('deleted_image').get('url').get('large')))
        self.assertFalse(
            os.path.isfile(data.get('deleted_image').get('url').get('medium')))
        self.assertFalse(
            os.path.isfile(data.get('deleted_image').get('url').get('thumb')))


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
