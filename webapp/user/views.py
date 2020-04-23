from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from webapp.user.forms import LoginForm
from webapp.user.forms import RegistrationForm
from webapp.user.forms import SelectTeacherStudentForm, StopTeacherForm, StopStudentForm
from webapp.user.models import User, Teacher, Student, TeacherStudent


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


def check_teacher_student(user_id):
    if Teacher.query.filter(Teacher.user_id == user_id).count():
        user_status = 'Teacher'
    elif Student.query.filter(Student.user_id == user_id).count():
        user_status = 'Student'
    else:
        user_status = 'User'
    return user_status


@blueprint.route('/user/<username>')
@login_required
def user(username):
    username = User.query.filter_by(username=username).first_or_404()
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    return render_template('user/user_page.html', user=username, user_id=user_id, user_status=user_status)


@blueprint.route('/select-tch-std/<username>', methods=['GET', 'POST'])
@login_required
def select_tch_std(username):
    select_form = SelectTeacherStudentForm()
    stop_teacher_form = StopTeacherForm()
    stop_student_form = StopStudentForm()
    username = User.query.filter_by(username=username).first_or_404()
    page_title = "Настройки профиля"
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    if select_form.validate_on_submit():
        user_choice = select_form.select_tch_std.data
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
        print(select_form.errors)
    return render_template('user/edit_profile.html',
                           select_form=select_form,
                           stop_teacher_form=stop_teacher_form,
                           stop_student_form=stop_student_form,
                           title=page_title, user=username, user_status=user_status)


@blueprint.route('/stop-teacher/<username>', methods=['GET', 'POST'])
@login_required
def stop_teacher(username):
    select_form = SelectTeacherStudentForm()
    stop_teacher_form = StopTeacherForm()
    stop_student_form = StopStudentForm()
    username = User.query.filter_by(username=username).first_or_404()
    page_title = "Настройки профиля"
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    if stop_teacher_form.validate_on_submit():
        teacher = Teacher.query.filter_by(user_id=user_id).first()
        db.session.delete(teacher)
        db.session.commit()
        flash('Вы перестали быть учителем!')
        return redirect(url_for('user.user', username=current_user.username))
    else:
        print(stop_teacher_form.errors)
    return render_template('user/edit_profile.html',
                           select_form=select_form,
                           stop_teacher_form=stop_teacher_form,
                           stop_student_form=stop_student_form,
                           title=page_title, user=username, user_status=user_status)


@blueprint.route('/stop-student/<username>', methods=['GET', 'POST'])
@login_required
def stop_student(username):
    select_form = SelectTeacherStudentForm()
    stop_teacher_form = StopTeacherForm()
    stop_student_form = StopStudentForm()
    username = User.query.filter_by(username=username).first_or_404()
    page_title = "Настройки профиля"
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    if stop_student_form.validate_on_submit():
        student = Student.query.filter_by(user_id=user_id).first()
        db.session.delete(student)
        db.session.commit()
        flash('Вы перестали быть учеником!')
        return redirect(url_for('user.user', username=current_user.username))
    else:
        print(stop_student_form.errors)
    return render_template('user/edit_profile.html',
                           select_form=select_form,
                           stop_teacher_form=stop_teacher_form,
                           stop_student_form=stop_student_form,
                           title=page_title, user=username, user_status=user_status)


@blueprint.route('/teacher-add-student/<username>', methods=['GET', 'POST'])
@login_required
def teacher_add_student(username):
    username = User.query.filter_by(username=username).first_or_404()
    title = 'Добавить ученика'
    add_student_form = AddStudentForm
    user_id = current_user.get_id()
    user_status = check_teacher_student(user_id)
    teacher = Teacher.query.filter(Teacher.user_id == user_id).first()
    teacher_id = teacher.teacher_id
    if form.validate_on_submit():
        student_username = User(student_username=add_student_form.student_username.data)  # имя студента из формы
        if TeacherStudent.query.filter(TeacherStudent.teacher_id == teacher_id).count() > 0:  # если учитель уже добавлял учеников
            teachers_students = TeacherStudent.query.filter(TeacherStudent.teacher_id == teacher_id).all()  # достаем все записи с учениками для данного учителя
            for teacher_student in teachers_students:  # для каждой записи проверяем
                st_user = User.query.filter(User.username == student_username).first()  #  из таблицы User достаем запись по имени ученика
                st_user_id = st_user.id  # по имени ученика получаем id ученика
                if teacher_student.student_id == st_user_id:
                    flash('Этот ученик уже добавлен в список ваших учеников!')
                    return redirect(url_for('user.teacher_add_student', username=current_user.username))

                teacher.students.append(s)
                db.session.add(t)
                db.session.commit()

    def teacher_has_student():
        user_id = current_user.get_id()
        teacher = Teacher.query.filter(Teacher.user_id == user_id).first()
        teacher_id = teacher.teacher_id
        if TeacherStudent.query.filter(TeacherStudent.teacher_id == teacher_id).count() > 0:
            teachers_students = TeacherStudent.query.filter(TeacherStudent.teacher_id == teacher_id).all()
            for teacher_student in teachers_students:
                student_id = teacher_student.student_id
                if student_id ==
                    student_id = st.student_id
                print(student_id)
        else:
            print('Вас нет в таблице teachers_students')

    return render_template('user/teacher_add_student.html',
                           add_student_form=add_student_form,
                           page_title=title, user=username, user_status=user_status)

def teacher_add_student(t_id, s_id):
    with app.app_context():
        t = Teacher.query.filter(Teacher.user_id == t_id).first()
        print(t)
        s = Student.query.filter(Student.user_id == s_id).first()
        print(s)
        t.students.append(s)
        db.session.add(t)
        db.session.commit()
        return f'Учитель с id {t_id} добавил ученика {s_id}'


