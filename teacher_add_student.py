from webapp import create_app
from webapp.db import db
from webapp.user.models import Student, Teacher

app = create_app()


def teacher_add_student(t_id, s_id):
    with app.app_context():
        t = Teacher.query.filter(Teacher.user_id == t_id).first()
        print(t)
        s = Student.query.filter(Student.user_id == s_id).first()
        print(s)
        t.students.append(s)
        db.session.add(t)
        db.session.commit()
        return f'Учитель с id {t_id} добавил ученика {s_id}'


if __name__ == '__main__':
    user_teacher_id = input('Введите user id учителя: ')
    user_student_id = input('Введите user id ученика: ')
    print(teacher_add_student(user_teacher_id, user_student_id))
