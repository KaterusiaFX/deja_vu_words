from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
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


class EditProfileForm(FlaskForm):
    teacher_choose = BooleanField('Я учитель', default=True, render_kw={"class": "form-check-input"})
    student_choose = BooleanField('Я ученик', default=True, render_kw={"class": "form-check-input"})
    submit = SubmitField('Внести', render_kw={"class": "btn btn-info"})


