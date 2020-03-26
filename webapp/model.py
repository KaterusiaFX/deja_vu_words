from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UsersWords(db.Model, UserMixin):
    __tabename__ = 'users_words'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    engword_id = db.Column(db.Integer, db.ForeignKey('English_words.id'))
    frenchword_id = db.Column(db.Integer, db.ForeignKey('French_words.id'))
    user_engword_id = db.Column(db.Integer, db.ForeignKey('English_words_added_by_users.id'))
    user_frenchword_id = db.Column(db.Integer, db.ForeignKey('French_words_added_by_users.id'))

    users = db.relationship('User', backref='users')
    english_words = db.relationship('EnglishWord', backref='english_words')
    french_words = db.relationship('FrenchWord', backref='french_words')
    user_english_words = db.relationship('EnglishWordOfUser', backref='user_english_words')
    user_french_words = db.relationship('FrenchWordOfUser', backref='user_french_words')


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


class EnglishWordOfUser(db.Model):
    __tablename__ = 'English_words_added_by_users'
    id = db.Column(db.Integer, primary_key=True)
    word_itself = db.Column(db.String, nullable=False)
    user = db.Column(db.String, nullable=False)
    translation_rus = db.Column(db.String, nullable=False)
    transcription = db.Column(db.String, nullable=True)
    audio_url = db.Column(db.String, unique=True, nullable=True)
    picture_url = db.Column(db.String, unique=True, nullable=True)
    imported_time = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<Word "{self.word_itself}" added by user {self.user} in English language>'


class FrenchWordOfUser(db.Model):
    __tablename__ = 'French_words_added_by_users'
    id = db.Column(db.Integer, primary_key=True)
    word_itself = db.Column(db.String, nullable=False)
    user = db.Column(db.String, nullable=False)
    translation_rus = db.Column(db.String, nullable=False)
    transcription = db.Column(db.String, nullable=True)
    feminine_or_masculine = db.Column(db.String, nullable=True)
    french_verb_group = db.Column(db.String, nullable=True)
    audio_url = db.Column(db.String, unique=True, nullable=True)
    picture_url = db.Column(db.String, unique=True, nullable=True)
    imported_time = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<Word "{self.word_itself}" added by user {self.user} in French language>'
