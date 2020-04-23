from webapp.db import db
from flask_login import current_user
from webapp.user.models import User, Student, Teacher, TeacherStudent


def teacher_has_student():
    user_id = current_user.get_id()
    teacher = Teacher.query.filter(Teacher.user_id == user_id).first()
    teacher_id = teacher.teacher_id
    username =
    user_id_from_username = User.query.filter(User)
    if TeacherStudent.query.filter(TeacherStudent.teacher_id == teacher_id).count() > 0:
        teachers_students = TeacherStudent.query.filter(TeacherStudent.teacher_id == teacher_id).all()
        for teacher_student in teachers_students:
            student_id = teacher_student.student_id
            if student_id ==
            student_id = st.student_id
            print(student_id)
    else:
        print('Вас нет в таблице teachers_students')


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

