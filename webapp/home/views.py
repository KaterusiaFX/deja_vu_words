from flask import Blueprint, render_template

blueprint = Blueprint('home', __name__)


@blueprint.route('/')
@blueprint.route('/index')
def index():
    title = 'Домой'
    return render_template('home.html', page_title=title)