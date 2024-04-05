from flask import Flask, flash, redirect, render_template, url_for
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

import config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__, static_url_path="/static")
    csrf = CSRFProtect()
    csrf.init_app(app)

    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)

    from app.models import models
    from app.routes import auth, recipe

    app.register_blueprint(auth.bp)
    app.register_blueprint(recipe.bp)

    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        # Flash a message to the user
        flash("You must be logged in to view that page.")
        return redirect(url_for("unauthorized_access"))

    @app.route("/unauthorized")
    def unauthorized_access():
        return render_template("unauthorized.html"), 401

    @app.context_processor
    def inject_user_status():
        # Assume 'user_id' in session is your criteria for being logged in

        is_logged_in = current_user.is_authenticated
        return dict(is_logged_in=is_logged_in)

    return app
