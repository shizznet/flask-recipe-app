from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

from app import db
from app.models import models
from config import AUTH_LOGIN


def generate_breadcrumbs():
    breadcrumbs = [{"url": "/", "text": "Home"}]  # Default breadcrumb for home page

    # Extract the path from the request URL
    path = request.path.strip("/").split("/")

    # Iterate over the path segments and generate breadcrumbs
    url_so_far = "/"
    for segment in path:
        url_so_far += segment + "/"
        breadcrumbs.append(
            {"url": "/" + url_so_far.strip("/"), "text": segment.capitalize()}
        )

    return breadcrumbs


class RegisterForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=4, max=25)])
    password = PasswordField(
        "New Password",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Repeat Password")


class LoginForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=4, max=25)])
    password = PasswordField("Password", [validators.DataRequired()])


bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    breadcrumbs = generate_breadcrumbs()
    form = RegisterForm()
    if form.validate_on_submit():
        print("inside form submit register")
        user = models.User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for(AUTH_LOGIN))
    return render_template("register.html", form=form, breadcrumbs=breadcrumbs)


@bp.route("/login", methods=["GET", "POST"])
def login():
    breadcrumbs = generate_breadcrumbs()
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for(AUTH_LOGIN))
        login_user(user)
        return redirect(url_for("recipe.view_recipes"))
    return render_template("login.html", form=form, breadcrumbs=breadcrumbs)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(AUTH_LOGIN))
