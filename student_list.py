from webapp import create_app
from webapp.user.models import User, Student, TeacherStudent

app = create_app()


def student_list(teacher):
    with app.app_context():
        teachers_students = TeacherStudent.query.filter(TeacherStudent.teacher_id == teacher).all()
        list_of_students = []
        for teacher_student in teachers_students:
            student_id = teacher_student.student_id
            student_in_student = Student.query.filter(Student.student_id == student_id).first()
            student_user_id = student_in_student.user_id
            student_in_user = User.query.filter(User.id == student_user_id).first()
            student_name = student_in_user.username
            list_of_students.append(student_name)
        student_list_len = len(list_of_students)
        return list_of_students, student_list_len


if __name__ == '__main__':
    teacher_id = input('Введите id учителя: ')
    print(student_list(teacher_id))
