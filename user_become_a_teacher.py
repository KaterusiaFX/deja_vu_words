import sys

from webapp import create_app

from webapp.db import db
from webapp.user.models import User, Teacher, Student

app = create_app()

with app.app_context():
    user_id = input('Введите user id')

    if User.query.filter(User.id == user_id).count():
        if Student.query.filter(Student.user_id == user_id).count():
            print('Вы уже зарегистрированы как студент и не можете стать учителем')
            sys.exit(0)
        if Teacher.query.filter(Teacher.user_id == user_id).count():
            print('Вы уже зарегистрированы как учитель')
            sys.exit(0)
        new_teacher = Teacher(user_id=user_id)
        db.session.add(new_teacher)
        db.session.commit()
        print('Создан пользователь с teacher_id={}'.format(new_teacher.teacher_id))
    else:
        print('Пользователя с таким id нет в базе данных')
