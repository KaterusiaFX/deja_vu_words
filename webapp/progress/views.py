from flask import Blueprint, render_template
from flask_login import current_user
import locale
import platform

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
