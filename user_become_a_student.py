import sys

from webapp import create_app

from webapp.db import db
from webapp.user.models import User, Student, Teacher

app = create_app()


def register_a_student(user_id):
    with app.app_context():
        if User.query.filter(User.id == user_id).count():
            if Teacher.query.filter(Teacher.user_id == user_id).count():
                return 'Вы уже зарегистрированы как учитель и не можете стать студентом'
                sys.exit(0)
            if Student.query.filter(Student.user_id == user_id).count():
                return 'Вы уже зарегистрированы как студент'
                sys.exit(0)
            new_student = Student(user_id=user_id)
            db.session.add(new_student)
            db.session.commit()
            return 'Создан пользователь с student_id={}'.format(new_student.student_id)
        else:
            return 'Пользователя с таким id нет в базе данных'


if __name__ == '__main__':
    user_id = input('Введите user id: ')
    print(register_a_student(user_id))
