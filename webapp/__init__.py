from flask import Flask
from flask import render_template
from webapp.forms import LoginForm
from webapp.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('index.html', title='Home')

    @app.route('/login')
    def login():
        form = LoginForm()
        return render_template('login.html', title='Sign In', form=form)

    return app