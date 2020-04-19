from datetime import datetime

from webapp.db import db


class UsersWords(db.Model):
    __tabename__ = 'users_words'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    engword_id = db.Column(db.Integer, db.ForeignKey('English_words.id'))
    frenchword_id = db.Column(db.Integer, db.ForeignKey('French_words.id'))
    user_engword_id = db.Column(db.Integer, db.ForeignKey('English_words_added_by_users.id'))
    user_frenchword_id = db.Column(db.Integer, db.ForeignKey('French_words_added_by_users.id'))
    imported_time = db.Column(db.DateTime, nullable=True, default=datetime.now())
    status = db.Column(db.String, nullable=True, default='new')
    memorizing_time = db.Column(db.DateTime, nullable=True)
    word_translation = db.Column(db.Integer, nullable=True, default=0)

    users = db.relationship('User', backref='users')
    english_words = db.relationship('EnglishWord', backref='english_words')
    french_words = db.relationship('FrenchWord', backref='french_words')
    user_english_words = db.relationship('EnglishWordOfUser', backref='user_english_words')
    user_french_words = db.relationship('FrenchWordOfUser', backref='user_french_words')


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
