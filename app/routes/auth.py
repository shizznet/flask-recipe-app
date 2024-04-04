from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

from app import db
from app.models import models


def generate_breadcrumbs():
    breadcrumbs = [{'url': '/', 'text': 'Home'}]  # Default breadcrumb for home page

    # Extract the path from the request URL
    path = request.path.strip('/').split('/')

    # Iterate over the path segments and generate breadcrumbs
    url_so_far = '/'
    for segment in path:
        url_so_far += segment + '/'
        breadcrumbs.append({'url': "/" + url_so_far.strip('/'), 'text': segment.capitalize()})

    return breadcrumbs


class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])


bp = Blueprint('auth', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    breadcrumbs = generate_breadcrumbs()
    form = RegisterForm()
    if form.validate_on_submit():
        print("inside form submit register")
        user = models.User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return "Registration succesfull"
        return redirect(url_for('auth.login'))
    else:
        return form.errors
    return "Register Get PAGe"
    return render_template('register.html', form=form, breadcrumbs=breadcrumbs)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    breadcrumbs = generate_breadcrumbs()
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user)
        return redirect(url_for('recipe.view_recipes'))
    return render_template('login.html', form=form, breadcrumbs=breadcrumbs)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
