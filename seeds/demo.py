from random import randint

from faker import Faker as Generator
from flask_seeder import Seeder
from sqlalchemy import or_

from limbook_api.db import db_drop_and_create_all
from limbook_api.v1.comments import generate_comment
from limbook_api.v1.friends import generate_friend
from limbook_api.v1.image_manager import generate_image
from limbook_api.v1.permissions import generate_permission, Permission
from limbook_api.v1.posts import generate_post, Post
from limbook_api.v1.reacts import generate_react
from limbook_api.v1.roles import generate_role, Role
from limbook_api.v1.users import generate_user, User
from run import app

generator = Generator()


class DemoSeeder(Seeder):

    # run() will be called by Flask-Seeder
    def run(self):
        db_drop_and_create_all()

        # ========================================
        # Generate permissions and roles
        # ========================================
        r_and_p = app.config.get('INITIAL_ROLES_AND_PERMISSIONS')
        demo_user_password = app.config.get('DEMO_USER_PASSWORD')

        for role_slug, perm_slugs in r_and_p.items():
            p_list = []
            # generate/find permissions and add to list
            for perm_slug in perm_slugs:
                permission = Permission.query.filter(
                    Permission.slug == perm_slug
                ).first()

                if permission is None:
                    permission = generate_permission(
                        slug=perm_slug,
                        name=perm_slug.replace(':', ' ').replace(
                            '_', ' ').capitalize(),
                        description=perm_slug.replace(':', ' ').replace(
                            '_', ' ').capitalize()
                    )

                p_list.append(permission)
                print('Created Permission: ' + permission.slug)

            # generate role
            generate_role(
                slug=role_slug,
                name=role_slug.replace('_', ' ').capitalize(),
                description=role_slug.replace('_', ' ').capitalize(),
                permissions=p_list
            )
            print('Created Role: ' + role_slug)

        # ========================================
        # Generate users
        # ========================================

        # Generate 3 test users
        # -----------------------------------------
        admin = Role.query.filter(Role.slug == 'admin').first()
        generate_user(
            first_name="Admin",
            last_name="A",
            email="admin@gmail.com",
            email_verified=True,
            password=demo_user_password,
            role_id=admin.id
        )
        print('Created User: Admin')

        verified_user = Role.query.filter(Role.slug == 'user').first()
        generate_user(
            first_name="Verified",
            last_name="User",
            email="verified_user@gmail.com",
            email_verified=True,
            password=demo_user_password,
            role_id=verified_user.id
        )
        print('Created User: Verified User')

        unverified_user = Role.query.filter(
            Role.slug == 'unverified_user'
        ).first()

        generate_user(
            first_name="Unverified",
            last_name="User",
            email="unverified_user@gmail.com",
            email_verified=False,
            password=demo_user_password,
            role_id=unverified_user.id
        )
        print('Created User: Unverified User')

        # Generate random verified users
        # -----------------------------------------
        for i in range(0, 27):
            generate_user(email_verified=True, role_id=2)
        print('Created 27 random verified users')

        # ============================================================
        # Generate friends/friend-requests for test user
        # ============================================================

        users = User.query.filter(
            or_(
                User.email == 'admin@gmail.com',
                User.email == 'verified_user@gmail.com'
            )
        )

        for user in users:
            user_id = user.id

            # generate friends
            for j in range(4, 10):
                generate_friend(
                    requester_id=user_id,
                    receiver_id=j,
                    is_friend=True
                )

            # get friend requests
            for j in range(11, 15):
                generate_friend(
                    requester_id=j,
                    receiver_id=user_id,
                    is_friend=False
                )

            # send friend requests to other
            for j in range(16, 20):
                generate_friend(
                    requester_id=user_id,
                    receiver_id=j,
                    is_friend=False
                )
            print('Generate friends/friend-requests for test user')

            # ====================================================
            # Generate posts for test user
            # ====================================================
            for j in range(0, randint(5, 15)):
                images = [generate_image() for k in range(randint(0, 5))]
                generate_post(user_id=user_id, images=images)

            posts = Post.query.filter(Post.user_id == user_id).all()
            print('Generate posts for test user')

            # ====================================================
            # Generate comments for posts
            # ====================================================
            for post in posts:
                comments = [
                    generate_comment(
                        user_id=randint(6, 20),
                        post_id=post.id
                    ) for k in range(randint(1, 5))
                ]
                post.comments = comments
                post.update()
            print('Generated comments for posts')

            # ====================================================
            # Generate reacts for posts
            # ====================================================
            for post in posts:
                reacts = [
                    generate_react(
                        user_id=randint(6, 20),
                        post_id=post.id
                    ) for k in range(randint(1, 5))
                ]
                post.reacts = reacts
                post.update()

            print('Generated reacts for posts')


# Make the tests conveniently executable
if __name__ == "__main__":
    with app.app_context():
        demo = DemoSeeder()
        demo.run()
