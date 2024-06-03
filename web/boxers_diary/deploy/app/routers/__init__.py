def register_blueprints(app):
    from app.routers.main_routes import main_bp
    from app.routers.auth_routes import auth_bp
    from app.routers.blog_routes import blog_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
