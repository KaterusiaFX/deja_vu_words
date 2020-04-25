import sys
from webapp import create_app
from webapp.db import db
from webapp.user.models import User, Student, Teacher, TeacherStudent

app = create_app()


def teacher_add_student(student_username, user_id):
    with app.app_context():
        student = User.query.filter(User.username == student_username).first()  #  запись из User по имени студента
        student_username = student.username
        student_user_id = student.id  # id студента из User
        check_student = Student.query.filter(Student.user_id == student_user_id).first()
        student_id_student = check_student.student_id
        teacher = Teacher.query.filter(Teacher.user_id == user_id).first()
        teacher_id = teacher.teacher_id
        return (f'Запись из таблицы User {student},\n имя пользователя {student_username},\n '
                f'id юзера студента {student_user_id},\n запись из таблицы Student {check_student},\n '
                f'значение из таблицы Teacher {teacher},\n '
                f'id учителя {teacher_id},\n id студента из Student {student_id_student}\n')


if __name__ == '__main__':
    st_username = input('Введите username студента: ')
    userid = input('Введите id пользователя учителя: ')
    print(teacher_add_student(st_username, userid))