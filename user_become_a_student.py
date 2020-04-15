import sys

from webapp import create_app

from webapp.db import db
from webapp.user.models import User, Student, Teacher

app = create_app()


with app.app_context():
    user_id = input('Введите user id')

    if User.query.filter(User.id == user_id).count():
        if Teacher.query.filter(Teacher.user_id == user_id).count():
            print('Вы уже зарегистрированы как учитель и не можете стать студентом')
            sys.exit(0)
        if Student.query.filter(Student.user_id == user_id).count():
            print('Вы уже зарегистрированы как студент')
            sys.exit(0)
        new_student = Student(user_id=user_id)
        db.session.add(new_student)
        db.session.commit()
        print('Создан пользователь с student_id={}'.format(new_student.student_id))
    else:
        print('Пользователя с таким id нет в базе данных')

    def check_student(user_id):
        if Student.query.filter(Student.user_id == user_id).count():
            user_status = 'Student'
            return user_status

    user_status = check_student(user_id)
    print(user_status)









