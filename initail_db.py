"""
The entry point for the Flask application.
"""

import os

from dotenv import load_dotenv

from app import create_app, db

# Import models to ensure they are registered with SQLAlchemy
from app.models import Event, Registration, User

env = os.getenv("FLASK_ENV", "development")

if env == "production":
    if not os.path.exists(".env.production"):
        raise FileNotFoundError("Production .env file not found. Please create it.")
    load_dotenv(dotenv_path=".env.production")
else:
    if not os.path.exists(".env.local"):
        raise FileNotFoundError("Local .env file not found. Please create it.")
    load_dotenv(dotenv_path=".env.local")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")
