from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from webapp.user.models import User


class LoginForm(FlaskForm):

    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    remember_me = BooleanField('Запомнить меня', default=True, render_kw={"class": "form-check-input"})
    submit = SubmitField('Войти', render_kw={"class": "btn btn-info"})


class RegistrationForm(FlaskForm):

    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('E-mail', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')], render_kw={"class": "form-control"})
    submit = SubmitField('Регистрация', render_kw={"class": "btn btn-info"})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Такое имя пользователя уже существует')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Такой email адрес уже существует')


class AddStudentForm(FlaskForm):

    student_username = StringField('Добавить ученика', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Сохранить', render_kw={"class": "btn btn-info"})

    def validate_student_username(self, student_username):
        user = User.query.filter_by(username=student_username.data).first()
        if user is None:
            raise ValidationError('Ученик с таким именем не зарегистрирован на сайте')


class SelectTeacherStudentForm(FlaskForm):
    select_tch_std = RadioField('Label', choices=[('value', 'Я учитель'), ('value_two', 'Я ученик')], )
    submit = SubmitField('Сохранить', render_kw={"class": "btn btn-info"})


class StopTeacherForm(FlaskForm):
    stop_teacher = BooleanField('Не хочу быть учителем', default=True, render_kw={"class": "form-check-input"})
    submit = SubmitField('Сохранить', render_kw={"class": "btn btn-info"})


class StopStudentForm(FlaskForm):
    stop_student = BooleanField('Не хочу быть учеником', default=True, render_kw={"class": "form-check-input"})
    submit = SubmitField('Сохранить', render_kw={"class": "btn btn-info"})
