from flask import render_template  # модуль для работы с шаблонами html
from app import app  # из папки app импорт переменной app
from app.forms import LoginForm  # из папки app, из файла forms.py импор-ем класс LoginForm

@app.route('/')  # это описание пути для запуска приложения app
@app.route('/index')  # путь для запуска шаблона index
def index():
    return render_template('index.html', title='Home')

@app.route('/login')  # путь для запуска шаблона login (форма Войти)
def login():
    form = LoginForm()  # создан экземпляр объекта из класса loginForm
    return render_template('login.html', title='Sign In', form=form)  # отправляем объект form в шаблон login.html


