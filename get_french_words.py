from datetime import datetime

from french_dict_generator import french_dict_generator
from webapp import create_app
from webapp.db import db
from webapp.dictionary.models import FrenchWord

app = create_app()


def save_words_in_db(words_dict):
    for word in words_dict:
        word_exist = FrenchWord.query.filter(FrenchWord.word_itself == word).count()
        if not word_exist:
            new_word = FrenchWord(
                word_itself=word,
                translation_rus=words_dict[word],
                imported_time=datetime.now()
                )
            db.session.add(new_word)
    db.session.commit()


words_dict = french_dict_generator()

if __name__ == "__main__":
    with app.app_context():
        save_words_in_db(words_dict)