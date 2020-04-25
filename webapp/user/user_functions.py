from webapp.db import db
from webapp.user.models import User, Teacher, Student, TeacherStudent


def check_teacher_student(user_id):
    if Teacher.query.filter(Teacher.user_id == user_id).count():
        user_status = 'Teacher'
    elif Student.query.filter(Student.user_id == user_id).count():
        user_status = 'Student'
    else:
        user_status = 'User'
    return user_status


def student_list(teacher):
    teachers_students = TeacherStudent.query.filter(TeacherStudent.teacher_id == teacher).all()
    list_of_students = []
    for teacher_student in teachers_students:
        student_id = teacher_student.student_id
        student_in_student = Student.query.filter(Student.student_id == student_id).first()
        student_user_id = student_in_student.user_id
        student_in_user = User.query.filter(User.id == student_user_id).first()
        student_name = student_in_user.username
        list_of_students.append(student_name)
    return list_of_students
