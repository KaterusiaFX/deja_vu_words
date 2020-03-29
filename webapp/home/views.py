from flask import Blueprint, render_template

blueprint = Blueprint('home', __name__)


@blueprint.route('/')
@blueprint.route('/index')
def index():
    title = 'Домашняя страница'
    return render_template('home/index.html', page_title=title)
