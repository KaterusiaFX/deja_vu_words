from flask import Blueprint, render_template
from flask_login import current_user
import locale
import platform

from webapp.progress.diagrams_functions import difficult_engwords_catplot, difficult_frenchwords_catplot
from webapp.progress.diagrams_functions import familiar_engwords_accumulated, familiar_frenchwords_accumulated
from webapp.progress.diagrams_functions import new_engwords_accumulated, new_frenchwords_accumulated
from webapp.user.views import check_teacher_student

blueprint = Blueprint('progress', __name__, url_prefix='/progress')

if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, 'russian')
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU')


@blueprint.route('/choose_diagram/<username>')
def choose_diagram(username):
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    return render_template('progress/choose_diagram.html', user_status=user_status)


@blueprint.route('/new_engwords/<username>')
def new_engwords(username):
    title = 'Рост числа английских слов в вашем словаре'
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    diagram = new_engwords_accumulated(username)
    return render_template(
        'progress/new_engwords.html',
        page_title=title,
        diagram=diagram,
        user_status=user_status
        )


@blueprint.route('/familiar_engwords/<username>')
def familiar_engwords(username):
    title = 'Рост числа изученных английских слов '
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    diagram = familiar_engwords_accumulated(username)
    return render_template(
        'progress/familiar_engwords.html',
        page_title=title,
        diagram=diagram,
        user_status=user_status
        )


@blueprint.route('/difficult_engwords/<username>')
def difficult_engwords(username):
    title = 'Самые сложные английские слова (не более 20 слов)'
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    diagram = difficult_engwords_catplot(username)
    return render_template(
        'progress/difficult_engwords.html',
        page_title=title,
        diagram=diagram,
        user_status=user_status
        )


@blueprint.route('/new_frenchwords/<username>')
def new_frenchwords(username):
    title = 'Рост числа французских слов в вашем словаре'
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    diagram = new_frenchwords_accumulated(username)
    return render_template(
        'progress/new_frenchwords.html',
        page_title=title,
        diagram=diagram,
        user_status=user_status
        )


@blueprint.route('/familiar_frenchwords/<username>')
def familiar_frenchwords(username):
    title = 'Рост числа изученных французских слов '
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    diagram = familiar_frenchwords_accumulated(username)
    return render_template(
        'progress/familiar_frenchwords.html',
        page_title=title,
        diagram=diagram,
        user_status=user_status
        )


@blueprint.route('/difficult_frenchwords/<username>')
def difficult_frenchwords(username):
    title = 'Самые сложные французские слова (не более 20 слов)'
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    diagram = difficult_frenchwords_catplot(username)
    return render_template(
        'progress/difficult_frenchwords.html',
        page_title=title,
        diagram=diagram,
        user_status=user_status
        )
