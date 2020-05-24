from random import randint

from faker import Faker as Generator
from flask_seeder import Seeder

from limbook_api.db import db_drop_and_create_all
from limbook_api.v1.comments import generate_comment
from limbook_api.v1.image_manager import generate_image
from limbook_api.v1.posts import generate_post, Post
from limbook_api.v1.reacts import generate_react
from run import app

generator = Generator()


class DemoSeeder(Seeder):

    # run() will be called by Flask-Seeder
    def run(self):
        db_drop_and_create_all()

        # ====================================================
        # Generate posts for test user
        # ====================================================
        user_ids = [
            'auth0|5eb669b054b14c0c128812e1',
            'auth0|5eb66a2d1cc1ac0c1496c16f'
        ]

        for user_id in user_ids:
            for j in range(0, randint(5, 15)):
                images = [
                    generate_image(user_id=user_id)
                    for k in range(randint(0, 5))
                ]
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
