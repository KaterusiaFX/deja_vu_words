from flask import render_template
from app import app
from app.forms import LoginForm  # из папки app, из файла forms.py импор-ем класс LoginForm

@app.route('/')  # это описание пути для приложения app
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login')  # по этому пути будут запускаться формы
def login():
    form = LoginForm()  # создан экземпляр объекта из класса loginForm
    return render_template('login.html', title='Sign In', form=form)  # отправляем объект form в шаблон login.html


