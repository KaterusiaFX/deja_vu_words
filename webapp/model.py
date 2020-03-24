from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


users_englishwords = db.Table('users_englishwords', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('engword_id', db.Integer, db.ForeignKey('English_words.id'))
    )


users_frenchwords = db.Table('users_frenchwords', 
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('frenchword_id', db.Integer, db.ForeignKey('French_words.id'))
    )


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(10), index=True)
    english_words = db.relationship('EnglishWord', secondary=users_englishwords, backref='english_words')
    french_words = db.relationship('FrenchWord', secondary=users_frenchwords, backref='french_words')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return '<User {}>'.format(self.username)


class EnglishWord(db.Model):
    __tablename__ = 'English_words'
    id = db.Column(db.Integer, primary_key=True)
    word_itself = db.Column(db.String, unique=True, nullable=False)
    translation_rus = db.Column(db.String, nullable=False)
    transcription = db.Column(db.String, nullable=True)
    audio_url = db.Column(db.String, unique=True, nullable=True)
    picture_url = db.Column(db.String, unique=True, nullable=True)
    imported_time = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<Word "{self.word_itself}" in English language>'


class FrenchWord(db.Model):
    __tablename__ = 'French_words'
    id = db.Column(db.Integer, primary_key=True)
    word_itself = db.Column(db.String, unique=True, nullable=False)
    translation_rus = db.Column(db.String, nullable=False)
    transcription = db.Column(db.String, nullable=True)
    feminine_or_masculine = db.Column(db.String, nullable=True)
    french_verb_group = db.Column(db.String, nullable=True)
    audio_url = db.Column(db.String, unique=True, nullable=True)
    picture_url = db.Column(db.String, unique=True, nullable=True)
    imported_time = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<Word "{self.word_itself}" in French language>'

