from datetime import datetime
from model import db, Word

from googletrans import Translator
translator = Translator()


def eng_dict_generator():
    english_list = [
                    'cat',
                    'kitten',
                    'dog',
                    'duck',
                    'cow',
                    'puppy',
                    'goat',
                    'frog',
                    'chicken',
                    'bee',
                    'whale',
                    'insect',
                    'rabbit',
                    'beaver',
                    'camel',
                    'crocodile',
                    'dolphin',
                    'fox',
                    'gorilla',
                    'hamster'
    ]

    russian_list = []

    english_dict = {}
    for word in english_list:
        translated = translator.translate(word, dest='ru')
        english_dict[word] = translated.text.lower()
        russian_list.append(translated.text.lower())

    save_words_in_db(english_dict)


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


if __name__ == '__main__':
    print(eng_dict_generator())
