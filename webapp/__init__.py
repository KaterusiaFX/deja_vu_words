from flask import Flask, render_template

from flask_login import LoginManager

from webapp.db import db
from webapp.admin.views import blueprint as admin_blueprint
from webapp.home.views import blueprint as home_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint
from webapp.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    app.register_blueprint(admin_blueprint)
    app.register_blueprint(home_blueprint)
    app.register_blueprint(user_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app

