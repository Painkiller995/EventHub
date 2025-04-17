import os

from dotenv import load_dotenv

# Load environment variables from .env files based on the environment
# -------------------------------------------------------------------
env = os.getenv("FLASK_ENV", "development")

if env == "production":
    if not os.path.exists(".env.production"):
        raise FileNotFoundError("Production .env file not found. Please create it.")
    load_dotenv(dotenv_path=".env.production")
else:
    if not os.path.exists(".env.local"):
        raise FileNotFoundError("Local .env file not found. Please create it.")
    load_dotenv(dotenv_path=".env.local")
# -------------------------------------------------------------------


class Config:
    """
    Configuration class for the Flask application.
    """

    # Flask configurations
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "app/static/uploads")

    # General configurations
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "your_security_password_salt")
    WTF_CSRF_ENABLED = os.getenv("WTF_CSRF_ENABLED", "True") == "True"

    # MySQL connection settings from environment variables
    MYSQL_HOST = os.getenv("MYSQL_HOST")
    MYSQL_PORT = os.getenv("MYSQL_PORT")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
    MYSQL_USER = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail Configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "1025"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "False") == "True"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False") == "True"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", None)
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", None)
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "noreply@eventhub.com")


config = Config()
