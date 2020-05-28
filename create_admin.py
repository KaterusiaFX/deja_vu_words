# Script for creating admin users
import sys

from getpass import getpass

from webapp import create_app
from webapp.db import db
from webapp.user.models import User

app = create_app()

with app.app_context():
    username = input('Введите имя пользователя ')

    if User.query.filter(User.username == username).count():
        print('Такой пользователь уже есть')
        sys.exit(0)

    email = input('Введите E-mail ')

    if User.query.filter(User.email == email).count():
        print('Такой E-mail уже существует')
        sys.exit(0)

    password1 = getpass('Введите пароль ')
    password2 = getpass('Повторите пароль ')

    if not password1 == password2:
        print('Пароли не совпадают')
        sys.exit(0)

    new_user = User(username=username, email=email, role='admin')
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print('Создан пользователь с id={}'.format(new_user.id))