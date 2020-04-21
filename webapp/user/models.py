from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.db import db

from sqlalchemy.orm import relationship


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)

    english_words = db.relationship('EnglishWord', secondary='users_words')
    french_words = db.relationship('FrenchWord', secondary='users_words')
    user_english_words = db.relationship('EnglishWordOfUser', secondary='users_words')
    user_french_words = db.relationship('FrenchWordOfUser', secondary='users_words')

    teacher = db.relationship('Teacher', backref='user', uselist=False)
    student = db.relationship('Student', backref='user', uselist=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Teacher(db.Model, UserMixin):
    __tablename__ = 'teachers'
    teacher_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    student_tch = db.relationship('TeacherStudent', backref='teachers')

    def __repr__(self):
        return f'<Teacher "{self.teacher_id}" has user id {self.user_id}>'

    def get_id(self):
        return set(self.teacher_id)


class Student(db.Model, UserMixin):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    teacher_std = db.relationship('TeacherStudent', backref='students')

    def __repr__(self):
        return f'<Student "{self.student_id}" has user id {self.user_id}>'

    def get_id(self):
        return set(self.student_id)


class TeacherStudent(db.Model, UserMixin):
    __tablename__ = 'teachers_students'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.teacher_id', ondelete='CASCADE'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id', ondelete='CASCADE'), nullable=False)

    tch_has_std = db.relationship('Student', backref='teacher_std')
