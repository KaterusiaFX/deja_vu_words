import os
import secrets

from PIL import Image

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
    student_data = []
    list_of_students = []
    for teacher_student in teachers_students:
        student_id = teacher_student.student_id
        student_in_student = Student.query.filter(Student.student_id == student_id).first()
        student_user_id = student_in_student.user_id
        student_in_user = User.query.filter(User.id == student_user_id).first()
        student_name = student_in_user.username
        student_avatar = student_in_user.image_file
        student_data.append(student_name)
        student_data.append(student_avatar)
        list_of_students.append(student_data)
        student_data = []
    return list_of_students


def teacher_list(student):
    teachers_students = TeacherStudent.query.filter(TeacherStudent.student_id == student).all()
    teacher_data = []
    list_of_teachers = []
    for teacher_student in teachers_students:
        teacher_id = teacher_student.teacher_id
        teacher_in_teacher = Teacher.query.filter(Teacher.teacher_id == teacher_id).first()
        teacher_user_id = teacher_in_teacher.user_id
        teacher_in_user = User.query.filter(User.id == teacher_user_id).first()
        teacher_name = teacher_in_user.username
        teacher_avatar = teacher_in_user.image_file
        teacher_data.append(teacher_name)
        teacher_data.append(teacher_avatar)
        list_of_teachers.append(teacher_data)
        teacher_data = []
    return list_of_teachers


def save_picture(form_picture):
    way_upload = "webapp/static/profile_pics"
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(way_upload, picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
