from webapp import create_app
from english_dict_generator import eng_dict_generator
from datetime import datetime
from webapp.db import db
from webapp.dictionary.models import EnglishWord

app = create_app()


def save_words_in_db(words_dict):
    for word in words_dict:
        word_exist = EnglishWord.query.filter(EnglishWord.word_itself == word).count()
        if not word_exist:
            new_word = EnglishWord(
                word_itself=word, 
                translation_rus=words_dict[word], 
                imported_time=datetime.now()
                )
            db.session.add(new_word)
    db.session.commit()


words_dict = eng_dict_generator()

if __name__ == "__main__":
    with app.app_context():
        save_words_in_db(words_dict)
#    ниже пример того, как сделать запрос всех или конкретного слова в базе данных
#    print(EnglishWord.query.all())
#    print(EnglishWord.query.filter_by(word_itself='kitten').first())
