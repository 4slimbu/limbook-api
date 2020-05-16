from unittest import main

from flask import json

from limbook_api.v1.friends import Friend, generate_friend, \
    generate_friend_request
from tests.base import BaseTestCase, test_user_id, api_base


class FriendsTestCase(BaseTestCase):
    """This class represents the test case for Friends"""

    # Friends Tests ----------------------------------------
    def test_cannot_access_friends_routes_without_correct_permission(self):
        # get friends
        res = self.client().get(
            api_base
            + '/friends'
            + '?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # get friend requests
        res = self.client().get(
            api_base
            + '/friend-requests'
            + '?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # send friend requests
        res = self.client().post(
            api_base
            + '/friend-requests'
            + '?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # accept friend request
        res = self.client().patch(
            api_base
            + '/friend-requests/1'
            + '?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # delete friend
        res = self.client().delete(
            api_base
            + '/friends/1'
            + '?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

        # delete friend request
        res = self.client().delete(
            api_base
            + '/friend-requests/1'
            + '?mock_token_verification=True'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data.get('error_code'), 'no_permission')

    def test_can_get_friends(self):
        # given
        generate_friend(
            requester_id="auth|friend1",
            receiver_id=test_user_id
        )
        generate_friend(
            requester_id=test_user_id,
            receiver_id="auth|friend2"
        )
        generate_friend(
            requester_id="auth|other1",
            receiver_id="auth|other2"
        )

        # get request initiated by test_user
        res = self.client().get(
            api_base
            + '/friends'
            + '?mock_token_verification=True&permission=read:friends'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data.get('friends')), 2)
        self.assertEqual(Friend.query.count(), 3)

    def test_can_get_friend_requests(self):
        # given
        # Test user has receive 2 friend requests and other user has
        # received 1 request.
        generate_friend_request(
            requester_id="auth|friend1",
            receiver_id=test_user_id
        )
        generate_friend_request(
            requester_id="auth|friend2",
            receiver_id=test_user_id
        )
        generate_friend_request(
            requester_id="auth|other1",
            receiver_id="auth|other2"
        )

        # get request initiated by test_user
        res = self.client().get(
            api_base
            + '/friend-requests'
            + '?mock_token_verification=True&permission=read:friends'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data.get('friend-requests')), 2)
        self.assertEqual(Friend.query.count(), 3)

    def test_can_create_friend_request(self):
        # given
        user_id = "auth|friend"

        # create friend request initiated by test user
        res = self.client().post(
            api_base
            + '/friend-requests'
            + '?mock_token_verification=True&permission=create:friends',
            json={"user_id": user_id}
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('friend-request').items() >= {
            "requester_id": test_user_id,
            "receiver_id": user_id,
            "is_friend": False
        }.items())
        self.assertEqual(Friend.query.count(), 1)

    def test_receiver_can_accept_friend_request(self):
        """
        The receiver of friend request can update the "is_friend"
        field to true and accept friend request.
        """
        # given
        requester_id = "auth|friend"
        friend_request = generate_friend_request(
            requester_id=requester_id,
            receiver_id=test_user_id
        )

        # update request initiated by receiver
        res = self.client().patch(
            api_base
            + '/friend-requests/' + str(friend_request.id)
            + '?mock_token_verification=True&permission=update:friends'
        )
        data = json.loads(res.data)

        # assert
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data.get('friend-request').items() >= {
            "requester_id": requester_id,
            "receiver_id": test_user_id,
            "is_friend": True
        }.items())

    def test_requester_or_other_cannot_update_friend_request(self):
        """
        The requester or other user cannot update friends
        """
        # given
        receiver_id = "auth|friend"
        friend_request = generate_friend_request(
            requester_id=test_user_id,
            receiver_id=receiver_id
        )

        # update initiated by requester
        res = self.client().patch(
            api_base
            + '/friend-requests/' + str(friend_request.id)
            + '?mock_token_verification=True&permission=update:friends'
        )

        # assert
        self.assertEqual(res.status_code, 401)

    def test_other_user_cannot_delete_others_friend(self):
        # given
        friend = generate_friend(
            requester_id="auth|friend1",
            receiver_id="auth|friend2"
        )

        # delete request initiated by other user
        res = self.client().delete(
            api_base
            + '/friends/' + str(friend.id)
            + '?mock_token_verification=True&permission=delete:friends'
        )
        self.assertEqual(res.status_code, 401)

    def test_other_user_cannot_delete_others_friend_request(self):
        # given
        friend_request = generate_friend_request(
            requester_id="auth|friend1",
            receiver_id="auth|friend2"
        )

        # delete request initiated by other user
        res = self.client().delete(
            api_base
            + '/friend-requests/' + str(friend_request.id)
            + '?mock_token_verification=True&permission=delete:friends'
        )
        self.assertEqual(res.status_code, 401)

    def test_requester_can_end_friendship(self):
        """ Requester can end friendship
        """
        # given
        friend = generate_friend(
            requester_id=test_user_id,
            receiver_id="auth|friend"
        )

        # delete request initiated by requester
        res = self.client().delete(
            api_base
            + '/friends/' + str(friend.id)
            + '?mock_token_verification=True&permission=delete:friends'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('deleted_id'), friend.id)
        self.assertEqual(Friend.query.count(), 0)

    def test_receiver_can_end_friendship(self):
        """ Receiver can end friendship
        """
        # given
        friend = generate_friend(
            requester_id="auth|friend",
            receiver_id=test_user_id
        )

        # delete request initiated by receiver
        res = self.client().delete(
            api_base
            + '/friends/' + str(friend.id)
            + '?mock_token_verification=True&permission=delete:friends'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('deleted_id'), friend.id)
        self.assertEqual(Friend.query.count(), 0)

    def test_requester_can_delete_friend_request(self):
        """ Requester can delete friend request
        """
        # given
        friend_request = generate_friend_request(
            requester_id=test_user_id,
            receiver_id="auth|friend"
        )

        # delete request initiated by requester
        res = self.client().delete(
            api_base
            + '/friend-requests/' + str(friend_request.id)
            + '?mock_token_verification=True&permission=delete:friends'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('deleted_id'), friend_request.id)
        self.assertEqual(Friend.query.count(), 0)

    def test_receiver_can_delete_friend_request(self):
        """ Receiver can delete friend request
        """
        # given
        friend_request = generate_friend_request(
            requester_id="auth|friend",
            receiver_id=test_user_id
        )

        # delete request initiated by receiver
        res = self.client().delete(
            api_base
            + '/friend-requests/' + str(friend_request.id)
            + '?mock_token_verification=True&permission=delete:friends'
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('deleted_id'), friend_request.id)
        self.assertEqual(Friend.query.count(), 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    main()
