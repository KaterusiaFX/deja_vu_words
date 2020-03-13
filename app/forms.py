# В этом файле хранятся классы веб-форм.

from flask_wtf import FlaskForm  # модуль для работы с формами
from wtforms import StringField, PasswordField, BooleanField, SubmitField  # поля, которые будут в форме
from wtforms.validators import DataRequired  # модуль для работы с валидаторами форм


class LoginForm(FlaskForm):  # класс форм

    username = StringField('Имя пользователя', validators=[DataRequired()])  # для ввода имени. validator проверяет, что поле не отправелнно пустым.
    password = PasswordField('Пароль', validators=[DataRequired()])  # для ввода пароля
    remember_me = BooleanField('Запомнить меня')  # флажок "Запомнить меня"
    submit = SubmitField('Войти')  # форма для кнопки "Отправить"
