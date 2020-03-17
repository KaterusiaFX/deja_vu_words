from flask import Flask
from flask import render_template

from webapp.model import db
from webapp.forms import LoginForm
from webapp.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    @app.route('/')
    @app.route('/index')
    def index():
        title = 'Домой'
        return render_template('index.html', title=title)

    @app.route('/login')
    def login():
        title = 'Авторизация'
        login_form = LoginForm()
        return render_template('login.html', title=title, form=login_form)

    return app



