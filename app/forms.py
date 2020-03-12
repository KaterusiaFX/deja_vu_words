# В этом файле хранятся классы веб-форм.

from flask_wtf import FlaskForm  # модуль для работы с формами
from wtforms import StringField, PasswordField, BooleanField, SubmitField  # поля, которые будут в форме
from wtforms.validators import DataRequired  # модуль для работы с валидаторами форм


class LoginForm(FlaskForm):  # класс форм

    username = StringField('Username', validators=[DataRequired()])  # для ввода имени. validator проверяет, что поле не отправелнно пустым.
    password = PasswordField('Password', validators=[DataRequired()])  # для ввода пароля
    remember_me = BooleanField('Remember Me')  # флажок "Запомнить меня"
    submit = SubmitField('Sign In')  # форма для кнопки "Отправить"
