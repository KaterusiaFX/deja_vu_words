from webapp import create_app
from webapp.user.models import User, Teacher, TeacherStudent


app = create_app()


def teacher_list(student):
    with app.app_context():
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
            print(teacher_data)
            teacher_data = []
        teacher_list_len = len(list_of_teachers)
        return list_of_teachers, teacher_list_len


if __name__ == '__main__':
    student_id = input('Введите id ученика: ')
    print(teacher_list(student_id))
