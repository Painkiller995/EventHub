from flask import Flask
from flask_login import LoginManager


def configure_auth(app: Flask) -> None:
    """
    Function to load authentication routes and configurations.
    This function sets up the authentication blueprint, initializes the database,
    and configures the login manager for user sessions.
    """
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
