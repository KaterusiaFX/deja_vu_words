from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_itself = db.Column(db.String, unique=True, nullable=False)
    language = db.Column(db.String, nullable=False)
    translation_rus = db.Column(db.String, nullable=False)
    transcription = db.Column(db.String, nullable=True)
    feminine_or_masculine = db.Column(db.String, nullable=True)
    french_verb_group = db.Column(db.String, nullable=True)
    audio_url = db.Column(db.String, unique=True, nullable=True)
    picture_url = db.Column(db.String, unique=True, nullable=True)
    imported_time = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<Word "{self.word_itself}", {self.language} language>'