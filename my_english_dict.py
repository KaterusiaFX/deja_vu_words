from webapp import create_app
from webapp.model import db, Word
from datetime import datetime

app = create_app()


def my_english_dict(word):
    with app.app_context():
        word_exist = Word.query.filter(Word.word_itself == word).first()
        if not word_exist or word_exist.language != 'English':
            word_itself = word
            word_translation = input('''Этого слова нет в словаре.
Чтобы добавить его в словарь - введите его перевод на русский: ''')
            new_word = Word(
                word_itself=word_itself, 
                language='English', 
                translation_rus=word_translation, 
                imported_time=datetime.now()
                )
            db.session.add(new_word)
            db.session.commit()
            return f'Слово "{word}" добавлено в словарь.'
        elif word_exist and word_exist.language == 'English':
            return word_exist.id


if __name__ == "__main__":
    find_word = input('Искать слово: ')
    print(my_english_dict(find_word))
