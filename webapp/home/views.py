from flask import Blueprint, render_template, url_for


blueprint = Blueprint('home', __name__)


@blueprint.route('/')
@blueprint.route('/index')
def index():
    title = 'Приветствуем вас на Deja vu words'
    image_file = url_for('static', filename='header.jpg')
    image_file_learn = url_for('static', filename='learning.jpg')
    image_file_teacher = url_for('static', filename='teacher.jpg')
    image_file_student = url_for('static', filename='student.jpg')
    return render_template('home/index.html', page_title=title, image_file=image_file,
                           image_file_learn=image_file_learn, image_file_teacher=image_file_teacher,
                           image_file_student=image_file_student)
