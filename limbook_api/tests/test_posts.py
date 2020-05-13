import io
import os
from unittest import main

from flask import json

from limbook_api.image_manager import create_image, generate_img_in_bytes
from limbook_api.posts import create_post
from limbook_api.tests.base import BaseTestCase, test_user_id


class PostsTestCase(BaseTestCase):
    """This class represents the test case for Posts"""

    # Posts Tests ----------------------------------------
    def test_cannot_access_post_routes_without_correct_permission(self):
        # get posts
        res1 = self.client().get(
            '/posts?mock_token_verification=True')
        data1 = json.loads(res1.data)

        # create post
        res2 = self.client().post(
            '/posts?mock_token_verification=True')
        data2 = json.loads(res2.data)

        # update post
        res3 = self.client().patch(
            '/posts/1?mock_token_verification=True')
        data3 = json.loads(res3.data)

        # delete post
        res4 = self.client().delete(
            '/posts/1?mock_token_verification=True')
        data4 = json.loads(res4.data)

        # attach image to post
        res5 = self.client().post(
            '/posts/1/images?mock_token_verification=True')
        data5 = json.loads(res5.data)

        # get reacts
        res6 = self.client().get(
            '/posts/1/reacts'
            + '?mock_token_verification=True'
        )
        data6 = json.loads(res6.data)

        # toggle react
        res7 = self.client().post(
            '/posts/1/reacts/toggle'
            + '?mock_token_verification=True'
        )
        data7 = json.loads(res7.data)

        # assert
        self.assertEqual(res1.status_code, 401)
        self.assertEqual(data1.get('error_code'), 'no_permission')
        self.assertEqual(res2.status_code, 401)
        self.assertEqual(data2.get('error_code'), 'no_permission')
        self.assertEqual(res3.status_code, 401)
        self.assertEqual(data3.get('error_code'), 'no_permission')
        self.assertEqual(res4.status_code, 401)
        self.assertEqual(data4.get('error_code'), 'no_permission')
        self.assertEqual(res5.status_code, 401)
        self.assertEqual(data5.get('error_code'), 'no_permission')
        self.assertEqual(res6.status_code, 401)
        self.assertEqual(data6.get('error_code'), 'no_permission')
        self.assertEqual(res7.status_code, 401)
        self.assertEqual(data7.get('error_code'), 'no_permission')

    def test_can_get_posts(self):
        # given
        post = create_post()

        # make request
        res = self.client().get(
            '/posts'
            + '?mock_token_verification=True&permission=read:posts'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('posts')[0], post.format())

    def test_can_create_posts(self):
        # given
        post = {
            "content": "My new Post"
        }

        # make request
        res = self.client().post(
            '/posts?mock_token_verification=True&permission=create:posts',
            json=post
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('posts')[0]['content'], post['content'])
        self.assertEqual(
            data.get('posts')[0]['user_id'],
            test_user_id
        )

    def test_can_update_posts(self):
        # given
        post = create_post({
            "content": "My new post",
            "user_id": test_user_id
        })
        updated_post_content = {
            "content": "My Updated Content"
        }

        # make request
        res = self.client().patch(
            '/posts/' + str(post.id)
            + '?mock_token_verification=True&permission=update:posts',
            json=updated_post_content
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            data.get('posts')[0]['content'],
            updated_post_content['content']
        )

    def test_can_delete_posts(self):
        # given
        post = create_post({
            'content': 'My new post',
            'user_id': test_user_id
        })

        # make request
        res = self.client().delete(
            '/posts/' + str(post.id)
            + '?mock_token_verification=True&permission=delete:posts'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('deleted_post'), post.format())

    def test_cannot_add_others_images_to_post(self):
        """ Cannot add other user's images to own post

        Other user's image should not be accessible
        to current user and hence should not be able to
        assign it to own posts
        """
        # given
        post = create_post(user_id=test_user_id)
        image1 = create_image()
        image2 = create_image()
        data = {
            "image_ids": [image1.id, image2.id]
        }

        # make request
        res = self.client().post(
            '/posts/' + str(post.id) + '/images'
            + '?mock_token_verification=True&permission=update:posts',
            json=data
        )

        # assert
        self.assertEqual(res.status_code, 404)

    def test_can_add_own_images_to_post(self):
        # given
        post = create_post(user_id=test_user_id)
        image1 = create_image(user_id=test_user_id)
        image2 = create_image(user_id=test_user_id)
        data = {
            "image_ids": [image1.id, image2.id]
        }

        # make request
        res = self.client().post(
            '/posts/' + str(post.id) + '/images'
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
            '/images'
            + '?mock_token_verification=True&permission=create:images',
            data=data
        )
        image = json.loads(res.data).get('image')

        # create post
        post = create_post(user_id=test_user_id)
        data = {
            "image_ids": [image.get('id')]
        }

        # attach images to post
        res = self.client().post(
            '/posts/' + str(post.id) + '/images'
            + '?mock_token_verification=True&permission=update:posts',
            json=data
        )
        post_with_image = json.loads(res.data).get('post')

        # delete post
        res = self.client().delete(
            '/posts/' + str(post.id)
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

    def test_can_react_and_unreact_post(self):
        # given
        post = create_post()
        post_id = post.id

        # make request
        res = self.client().post(
            '/posts/' + str(post_id) + '/reacts/toggle'
            + '?mock_token_verification=True&permission=update:reacts'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('post').get('reacts')), 1)

        # make request
        res = self.client().post(
            '/posts/' + str(post_id) + '/reacts/toggle'
            + '?mock_token_verification=True&permission=update:reacts'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data.get('post').get('reacts')), 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
