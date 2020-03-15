from app import app
from english_dict_generator import eng_dict_generator
from datetime import datetime
from model import db, Word


def save_words_in_db(words_dict):
    for word in words_dict:
        word_exist = Word.query.filter(Word.word_itself == word).count()
        print(word_exist)
        if not word_exist:
            new_word = Word(
                word_itself=word, 
                language='English', 
                translation_rus=words_dict[word], 
                imported_time=datetime.now()
                )
            db.session.add(new_word)
            db.session.commit()


words_dict = eng_dict_generator()

with app.app_context():
    save_words_in_db(words_dict)
