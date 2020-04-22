import sys
from webapp import create_app
from webapp.db import db
from webapp.user.models import User, Student, Teacher, TeacherStudent

app = create_app()


with app.app_context():
    t = Teacher.query.filter(Teacher.teacher_id).first()
    print(t)
    s = Student.query.filter(Student.student_id).first()
    print(s)
    s.teacher_std.append(t)
    db.session.add(t)
    db.session.commit()


#class Teacher(db.Model, UserMixin): (Parent)
    #__tablename__ = 'teachers'
    #teacher_id = db.Column(db.Integer, primary_key=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    #student_tch = db.relationship('TeacherStudent', backref='teachers')



#class Student(db.Model, UserMixin): (Child)
    #__tablename__ = 'students'
    #student_id = db.Column(db.Integer, primary_key=True)
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    #teacher_std = db.relationship('TeacherStudent', backref='students')


#class TeacherStudent(db.Model, UserMixin): (Association)
   # __tablename__ = 'teachers_students'
    #id = db.Column(db.Integer, primary_key=True)
    #teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id', ondelete='CASCADE'), nullable=False)
    #student_id = db.Column(db.Integer, db.ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)

