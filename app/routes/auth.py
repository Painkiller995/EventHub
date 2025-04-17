from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import login_required, login_user, logout_user

from app import db
from app.auth_helpers import generate_verification_code, send_verification_email
from app.forms.auth import LoginForm, SignUpForm, VerifyAccountForm
from app.models import User

auth_routes = Blueprint("auth", __name__)


@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle login process.

    GET: Render the login form.
    POST: Validate the form and log in the user if valid.

    """
    form = LoginForm(request.form)

    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data

            user = User.query.filter_by(email=email).first()

            if not user or not user.check_password(password):
                flash("Please check your login details and try again.", "error")
                return redirect(url_for("auth.login"))

            if not user.is_verified:
                flash("Your account is not active. Please sign up or verify your email.", "error")
                return redirect(url_for("auth.login"))

            login_user(user, remember=remember)
            return redirect(url_for("event.my_events"))

        flash("Form validation failed. Please check your inputs.", "error")

    return render_template("./auth/login.html", form=form)


@auth_routes.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Handle signup process.

    GET: Render the signup form.
    POST: Validate the form and create a new user if valid.

    """
    form = SignUpForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            name = form.name.data
            password = form.password.data

            if not email or not name or not password:
                flash("All fields are required. Please fill in all fields.", "error")
                return redirect(url_for("auth.signup"))

            existing_user = User.query.filter_by(email=email).first()

            if existing_user:
                if existing_user.is_verified:
                    flash("This email is already registered and verified. Please log in.", "error")
                    return redirect(url_for("auth.login"))

                # Send verification code if user exists but is not verified
                verification_code = generate_verification_code()
                send_verification_email(email, verification_code)
                session["verification_code"] = verification_code
                session["email"] = email

                flash("A verification code has been sent to your email. Please check your inbox.", "success")
                return redirect(url_for("auth.verify_code"))

            # If the email is not in use, create a new user
            new_user = User()
            new_user.email = email
            new_user.name = name
            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            # Generate and send a verification code
            verification_code = generate_verification_code()
            send_verification_email(email, verification_code)

            session["verification_code"] = verification_code
            session["email"] = email

            flash("A verification code has been sent to your email. Please verify it to complete signup.", "success")
            return redirect(url_for("auth.verify_code"))

    return render_template("./auth/signup.html", form=form)


@auth_routes.route("/verify_code", methods=["GET", "POST"])
def verify_code():
    """
    Handle verification code process.

    GET: Render the verification code form.
    POST: Validate the code and activate the user's account if valid.

    """
    form = VerifyAccountForm()
    if request.method == "POST" and form.validate_on_submit():
        user_code = form.code.data
        email = session.get("email")

        if not user_code:
            flash("Please enter the verification code.", "error")
            return redirect(url_for("auth.verify_code"))

        stored_code = session.get("verification_code")
        if not stored_code:
            flash("No verification code found. Please try again.", "error")
            return redirect(url_for("auth.signup"))

        if user_code == stored_code:
            user = User.query.filter_by(email=email).first()
            if user:
                user.is_verified = True
                db.session.commit()
                flash("Signup successful! Your account is now verified and active.", "success")
                return redirect(url_for("auth.login"))
            else:
                flash("User not found. Please try again.", "error")
                return redirect(url_for("auth.signup"))
        else:
            flash("Invalid verification code. Please check your code and try again.", "error")
            return redirect(url_for("auth.verify_code"))

    return render_template("./auth/verify_code.html", form=form)


@auth_routes.route("/logout")
@login_required
def logout():
    """
    Handle logout process.
    Logs out the user and redirects to the main page.
    """
    logout_user()
    return redirect(url_for("main.index"))
