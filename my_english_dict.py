from webapp import create_app
from webapp.model import db, EnglishWord, User, users_words
from datetime import datetime

app = create_app()


def webapp_engdict_insert(word, user):
    with app.app_context():
        word_exist = EnglishWord.query.filter(EnglishWord.word_itself == word).first()
        if not word_exist:
            word_itself = word
            word_translation = input('''Этого слова нет в английском словаре.
Чтобы добавить его в английский словарь - введите его перевод на русский: ''')
            new_word = EnglishWord(
                word_itself=word_itself, 
                translation_rus=word_translation, 
                imported_time=datetime.now()
                )
            db.session.add(new_word)
            db.session.commit()
            insertion = user_engdict_insert(word, user)
            return f'{insertion} и в словарь на сайте.'
        return user_engdict_insert(word, user)
        

def user_engdict_insert(word, user):
    with app.app_context():
        word_exist = EnglishWord.query.filter(EnglishWord.word_itself == word).first()
        user_exist = User.query.filter(User.username == user).first()
        user_exist.english_words.append(word_exist)
        db.session.add(user_exist)
        db.session.commit()
        return f'Слово "{word}" добавлено в ваш словарь'


if __name__ == "__main__":
    find_word = input('Введите слово для поиска: ')
    user = input('Введите имя пользователя: ')
    print(webapp_engdict_insert(find_word, user))
