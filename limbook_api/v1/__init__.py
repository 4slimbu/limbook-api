def register_v1_blueprints(app):
    url_prefix = '/v1'
    from limbook_api.v1.auth.routes import auth
    from limbook_api.v1.posts.routes import posts
    from limbook_api.v1.reacts.routes import reacts
    from limbook_api.v1.comments.routes import comments
    from limbook_api.v1.activities.routes import activities
    from limbook_api.v1.image_manager.routes import image_manager
    from limbook_api.v1.friends.routes import friends
    from limbook_api.v1.users.routes import users
    app.register_blueprint(auth, url_prefix=url_prefix)
    app.register_blueprint(posts, url_prefix=url_prefix)
    app.register_blueprint(reacts, url_prefix=url_prefix)
    app.register_blueprint(comments, url_prefix=url_prefix)
    app.register_blueprint(activities, url_prefix=url_prefix)
    app.register_blueprint(image_manager, url_prefix=url_prefix)
    app.register_blueprint(friends, url_prefix=url_prefix)
    app.register_blueprint(users, url_prefix=url_prefix)
