from webapp import create_app
from webapp.db import db
from webapp.user.models import User, Student, Teacher, TeacherStudent
app = create_app()


user_teacher_id = input('Введите user id учителя: ')
user_id = input('Введите свой user_id')


with app.app_context():
    user_id = user_id
    teacher = Teacher.query.filter(Teacher.user_id == user_id).first()
    teacher_id = teacher.teacher_id
    print(f'Пользователя с id {user_id} соответствует id учителя {teacher_id}')
    if TeacherStudent.query.filter(TeacherStudent.teacher_id == user_teacher_id).count() > 0:  # проверяю, есть ли хоть одна запись в таблице TeacherStudent для данного учителя
        teachers_students = TeacherStudent.query.filter(TeacherStudent.teacher_id == user_teacher_id).all()  # достаю запись по данному учителю
        print(teachers_students)
        for st in teachers_students:
            student_id = st.student_id
            print(student_id)
    else:
        print('Вас нет в таблице teachers_students')
