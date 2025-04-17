from flask import Flask


def register_routes(app: Flask) -> None:
    """Function to register all routes (blueprints) with the app."""
    # Register the blueprints
    from .routes.main import main_routes

    app.register_blueprint(main_routes)

    # Register the blueprints
    from .routes.auth import auth_routes

    app.register_blueprint(auth_routes)

    # Register the blueprints
    from .routes.event import event_routes

    app.register_blueprint(event_routes)
