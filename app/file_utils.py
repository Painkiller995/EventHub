import os
import uuid

from flask import url_for
from werkzeug.utils import secure_filename

from .config import config

# Allowed extensions
ALLOWED_EXTENSIONS = {"png", "jpg"}


def allowed_file(filename):
    """Check if the file has an allowed image extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file):
    """Save uploaded file and return its accessible URL."""
    if file and allowed_file(file.filename):
        os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)

        ext = os.path.splitext(file.filename)[1]

        random_filename = f"{uuid.uuid4().hex}{ext}"

        filename = secure_filename(random_filename)

        file_path = os.path.join(config.UPLOAD_FOLDER, filename)

        file.save(file_path)

        # Return the URL to access the file
        return url_for("static", filename=f"uploads/{filename}")

    return None
