from flask import Blueprint, render_template
from flask_login import current_user, login_required

main_routes = Blueprint("main", __name__)


@main_routes.route("/")
def index():
    """Render the index page."""
    return render_template("./general/index.html")


@main_routes.route("/about")
def about():
    """Render the index page."""
    return render_template("./general/about.html")


@main_routes.route("/dashboard")
@login_required
def dashboard():
    """Render the dashboard page."""
    return render_template("./event/dashboard.html", name=current_user.name)
