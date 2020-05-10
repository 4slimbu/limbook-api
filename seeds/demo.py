from faker import Faker as Generator
from flask_seeder import Seeder

from limbook_api.db.model import db_drop_and_create_all, create_random_post

generator = Generator()


class DemoSeeder(Seeder):

    # run() will be called by Flask-Seeder
    def run(self):
        db_drop_and_create_all()

        # ====================
        # Drinks
        # ====================
        # Create 5 drinks
        for i in range(0, 15):
            create_random_post()
