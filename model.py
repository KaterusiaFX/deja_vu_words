from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route("/")
    def index():
        return 'Strrranichka'

    return app

db = SQLAlchemy()

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, unique=True, nullable=False)
    language = db.Column(db.String, nullable=False)
    translation_rus = db.Column(db.String, nullable=False)
    transcription = db.Column(db.String, nullable=True)
    audiofile = db.Column(db.LargeBinary, nullable=True)
    picture = db.Column(db.LargeBinary, nullable=True)
    imported = db.Column(db.DateTime, nullable=False)
    

    def __repr__(self):
        return f'<Word {self.title} in {self.language}>'

