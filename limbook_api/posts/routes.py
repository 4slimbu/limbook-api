from flask import Blueprint, render_template

posts = Blueprint('posts', __name__)


@posts.route("/")
def get_posts():
    return render_template('home.html')
