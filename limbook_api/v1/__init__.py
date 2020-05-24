def register_v1_blueprints(app):
    url_prefix = '/v1'
    from limbook_api.v1.auth.routes import auth
    from limbook_api.v1.stats.routes import stats
    from limbook_api.v1.posts.routes import posts
    from limbook_api.v1.reacts.routes import reacts
    from limbook_api.v1.comments.routes import comments
    from limbook_api.v1.image_manager.routes import image_manager
    app.register_blueprint(auth, url_prefix=url_prefix)
    app.register_blueprint(stats, url_prefix=url_prefix)
    app.register_blueprint(posts, url_prefix=url_prefix)
    app.register_blueprint(reacts, url_prefix=url_prefix)
    app.register_blueprint(comments, url_prefix=url_prefix)
    app.register_blueprint(image_manager, url_prefix=url_prefix)
