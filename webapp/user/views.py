from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from webapp.user.forms import LoginForm
from webapp.user.forms import RegistrationForm
from webapp.user.forms import SelectTeacherStudentForm, StopTeacherForm, StopStudentForm
from webapp.user.models import User, Teacher, Student


from webapp import db

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    title = 'Вход'
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы вошли на сайт')
            return redirect(url_for('home.index'))

    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('home.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    title = 'Регистрация'
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role='user')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', page_title=title, form=form)


@blueprint.route('/user/<username>')
@login_required
def user(username):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    return render_template('user/user_page.html', user=username, user_id=user_id)


@blueprint.route('/select-tch-std/<username>', methods=['GET', 'POST'])
@login_required
def select_tch_std(username):
    form = SelectTeacherStudentForm()
    username = User.query.filter_by(username=username).first_or_404()
    page_title = "Настройки профиля"
    if form.validate_on_submit():
        user_choice = form.select_tch_std.data
        user_id = current_user.get_id()
        if user_choice == 'value':
            if Teacher.query.filter(Teacher.user_id == user_id).count():
                flash('Вы уже регистрировались ранее как учитель!')
                return redirect(url_for('user.user', username=current_user.username))
            teacher = Teacher(user_id=user_id)
            db.session.add(teacher)
            db.session.commit()
            flash('Вы стали учителем!')
            return redirect(url_for('user.user', username=current_user.username))
        if user_choice == 'value_two':
            if Student.query.filter(Student.user_id == user_id).count():
                flash('Вы уже регистрировались ранее как ученик!')
                return redirect(url_for('user.user', username=current_user.username))
            student = Student(user_id=user_id)
            db.session.add(student)
            db.session.commit()
            flash('Вы стали учеником!')
            return redirect(url_for('user.user', username=current_user.username))
    else:
        print(form.errors)
    return render_template('user/edit_profile.html', user=username, title=page_title, form=form)


@blueprint.route('/stop-teacher/<username>', methods=['GET', 'POST'])
@login_required
def stop_teacher(username):
    form = StopTeacherForm()
    username = User.query.filter_by(username=username).first_or_404()
    page_title = "Настройки профиля"
    if form.validate_on_submit():
        user_id = current_user.get_id()
        Teacher.query.filter_by(user_id).delete()
        flash('Вы перестали быть учителем!')
        return redirect(url_for('user.user', username=current_user.username))
    else:
        print(form.errors)
    return render_template('user/edit_profile.html', user=username, title=page_title, form=form)


@blueprint.route('/stop-student/<username>', methods=['GET', 'POST'])
@login_required
def stop_student(username):
    form = StopStudentFormForm()
    username = User.query.filter_by(username=username).first_or_404()
    page_title = "Настройки профиля"
    if form.validate_on_submit():
        user_id = current_user.get_id()
        Student.query.filter_by(user_id).delete()
        flash('Вы перестали быть учеником!')
        return redirect(url_for('user.user', username=current_user.username))
    else:
        print(form.errors)
    return render_template('user/edit_profile.html', user=username, title=page_title, form=form)



















