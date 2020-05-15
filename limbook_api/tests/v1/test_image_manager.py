import io
import os
from unittest import main

from flask import json

from limbook_api.v1.image_manager import generate_img_in_bytes, generate_image
from limbook_api.v1.posts import generate_post
from limbook_api.tests.base import BaseTestCase
from limbook_api.tests.v1 import test_user_id, api_base


class ImageManagerTestCase(BaseTestCase):
    """This class represents the test case for Image Manager"""

    def test_cannot_access_image_routes_without_correct_permission(self):
        # create image
        res = self.client().post(
            api_base
            + '/images'
            + '?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # get image
        res = self.client().get(
            api_base
            + '/images/1'
            + '?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # get images
        res = self.client().get(
            api_base
            + '/images'
            + '?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # delete image
        res = self.client().delete(
            api_base
            + '/images/1'
            + '?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_cannot_retrieve_other_images(self):
        """ I can only retrieve my images """
        # given
        image = generate_image()

        # make request
        res = self.client().get(
            api_base
            + '/images'
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
        image1 = generate_image(user_id=test_user_id)
        image2 = generate_image(user_id=test_user_id)
        image3 = generate_image()
        image4 = generate_image()

        # make request
        res = self.client().get(
            api_base
            + '/images'
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
            api_base
            + '/images'
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
            api_base
            + '/images'
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
            api_base
            + '/images'
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
            api_base
            + '/images'
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
        image = generate_image()
        image_id = image.id

        # make request
        res = self.client().get(
            api_base
            + '/images/' + str(image_id)
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
        image = generate_image(
            user_id=test_user_id,
            url=json.dumps({
                "thumb": "thumb.jpg",
                "medium": "medium.jpg",
                "large": "large.jpg"
            })
        )

        # make request
        res = self.client().get(
            api_base
            + '/images/' + str(image.id)
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
        image = generate_image()

        # make request
        res = self.client().delete(
            api_base
            + '/images/' + str(image.id)
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
            api_base
            + '/images'
            + '?mock_token_verification=True&permission=create:images',
            data=data
        )
        image = json.loads(res.data).get('image')

        # make delete request
        res = self.client().delete(
            api_base
            + '/images/' + str(image.get('id'))
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

    # -------------------------------------------------
    # Test involving posts
    # -------------------------------------------------

    def test_cannot_access_post_image_routes_without_permission(self):
        # attach image to post
        res = self.client().post(
            api_base
            + '/posts/1/images?mock_token_verification=True')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_cannot_add_others_images_to_post(self):
        """ Cannot add other user's images to own post

        Other user's image should not be accessible
        to current user and hence should not be able to
        assign it to own posts
        """
        # given
        post = generate_post(user_id=test_user_id)
        image1 = generate_image()
        image2 = generate_image()
        data = {
            "image_ids": [image1.id, image2.id]
        }

        # make request
        res = self.client().post(
            api_base
            + '/posts/' + str(post.id) + '/images'
            + '?mock_token_verification=True&permission=update:posts',
            json=data
        )

        # assert
        self.assertEqual(res.status_code, 404)

    def test_can_add_own_images_to_post(self):
        # given
        post = generate_post(user_id=test_user_id)
        image1 = generate_image(user_id=test_user_id)
        image2 = generate_image(user_id=test_user_id)
        data = {
            "image_ids": [image1.id, image2.id]
        }

        # make request
        res = self.client().post(
            api_base
            + '/posts/' + str(post.id) + '/images'
            + '?mock_token_verification=True&permission=update:posts',
            json=data
        )

        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertEqual(data.get('post').get('images')[0], image1.format())
        self.assertEqual(data.get('post').get('images')[1], image2.format())

    def test_deleting_post_should_delete_images_as_well(self):
        # given
        # create image
        image = (io.BytesIO(generate_img_in_bytes()), 'test.jpg')
        data = {"image": image}

        # save image
        res = self.client().post(
            api_base
            + '/images'
            + '?mock_token_verification=True&permission=create:images',
            data=data
        )
        image = json.loads(res.data).get('image')

        # create post
        post = generate_post(user_id=test_user_id)
        data = {
            "image_ids": [image.get('id')]
        }

        # attach images to post
        res = self.client().post(
            api_base
            + '/posts/' + str(post.id) + '/images'
            + '?mock_token_verification=True&permission=update:posts',
            json=data
        )
        post_with_image = json.loads(res.data).get('post')

        # delete post
        res = self.client().delete(
            api_base
            + '/posts/' + str(post.id)
            + '?mock_token_verification=True&permission=delete:posts'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('deleted_post').get('id'), post_with_image.get('id'))
        self.assertEqual(len(data.get('deleted_post').get('images')), 0)
        self.assertFalse(
            os.path.isfile(image.get('url').get('large')))
        self.assertFalse(
            os.path.isfile(image.get('url').get('medium')))
        self.assertFalse(
            os.path.isfile(image.get('url').get('thumb')))


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
