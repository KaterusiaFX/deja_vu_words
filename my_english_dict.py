from webapp import create_app
from webapp.db import db 
from webapp.dictionary.models import EnglishWord, EnglishWordOfUser
from webapp.user.models import User
from datetime import datetime

app = create_app()


def webapp_engdict_insert(word, user):
    with app.app_context():
        word_exist_userdict = EnglishWordOfUser.query.filter(EnglishWordOfUser.word_itself == word).all()
        if word_exist_userdict:
            for user_word in word_exist_userdict:
                if user_word.user == user:
                    return f'Слово "{word}" уже есть в вашем словаре.'
        word_exist = EnglishWord.query.filter(EnglishWord.word_itself == word).first()
        if not word_exist:
            word_itself = word
            word_translation = input('''Этого слова нет в английском словаре.
Чтобы добавить его в английский словарь - введите его перевод на русский: ''')
            new_word = EnglishWordOfUser(
                word_itself=word_itself,
                user=user,
                translation_rus=word_translation, 
                imported_time=datetime.now()
                )
            db.session.add(new_word)
            db.session.commit()
            insertion = user_engdict_own_insert(word, user)
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


def user_engdict_own_insert(word, user):
    with app.app_context():
        word_exist = EnglishWordOfUser.query.filter(EnglishWordOfUser.word_itself == word).first()
        user_exist = User.query.filter(User.username == user).first()
        user_exist.user_english_words.append(word_exist)
        db.session.add(user_exist)
        db.session.commit()
        return f'Слово "{word}" добавлено в ваш словарь'


if __name__ == "__main__":
    find_word = input('Введите слово для поиска: ')
    user = input('Введите имя пользователя: ')
    print(webapp_engdict_insert(find_word, user))
