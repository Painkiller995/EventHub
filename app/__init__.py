"""
Flask application factory for the app module.
"""

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect  # Import CSRFProtect

from .auth_config import configure_auth
from .routes_manager import register_routes

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

# Initialize Bcrypt
bcrypt = Bcrypt()

# flask mail
mail = Mail()

# Initialize CSRF protection
csrf = CSRFProtect()


def create_app() -> Flask:
    """Create and configure the Flask application."""

    app = Flask(__name__)

    # Load configuration from environment variables
    app.config.from_object("app.config.Config")

    # Initialize the database with the app
    db.init_app(app)

    # Initialize Bcrypt with the app
    bcrypt.init_app(app)

    # Initialize Flask-Mail with the app
    mail.init_app(app)

    # Initialize CSRF protection with the app
    csrf.init_app(app)

    # Configure authentication
    configure_auth(app)

    # Register the routes (blueprints)
    register_routes(app)

    return app
