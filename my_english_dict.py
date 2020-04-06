from get_transcription import get_transcription
from webapp import create_app
from webapp.db import db
from webapp.dictionary.models import EnglishWord, EnglishWordOfUser, UsersWords
from webapp.user.models import User

from datetime import datetime
from translate import Translator

app = create_app()
translator = Translator(to_lang="ru")


def webapp_engdict_insert(word, user):
    with app.app_context():
        if not word and not user:
            return 'Вы не ввели слово и имя пользователя.'
        if not word:
            return 'Вы не ввели слово.'
        if not user:
            return 'Вы не ввели имя пользователя.'

        word_exist_userdict = EnglishWordOfUser.query.filter(EnglishWordOfUser.word_itself == word).all()
        word_exist = EnglishWord.query.filter(EnglishWord.word_itself == word).first()
        user_exist = User.query.filter(User.username == user).first()

        # проверка существования пользователя
        if not user_exist:
            return f'Пользователь {user} не зарегистрирован на сайте.'

        # проверка, есть ли у этого пользователя слова в его личном словаре
        user_words = UsersWords.query.filter(UsersWords.user_id == user_exist.id).all()

        # слово есть в словаре пользователя
        if user_words:
            if user_exist.is_admin and word_exist:
                for user_admin_word in user_words:
                    if user_admin_word.engword_id == word_exist.id:
                        return f'Слово "{word}" уже есть в вашем словаре, перевод: {word_exist.translation_rus}.'
            for user_not_admin_word in user_words:
                if word_exist and user_not_admin_word.engword_id == word_exist.id:
                    return f'Слово "{word}" уже есть в вашем словаре, перевод: {word_exist.translation_rus}.'
                if word_exist_userdict:
                    for every_word in word_exist_userdict:
                        if every_word.user == user and every_word.id == user_not_admin_word.user_engword_id:
                            return f'Слово "{word}" уже есть в вашем словаре, перевод: {every_word.translation_rus}.'

        # слова нет в словаре пользователя
        # слова нет в общем словаре (словарь, генерируемый админами)
        if not word_exist:
            word_autotranslation = translator.translate(word)
            translation_accept = input(f'''Этого слова нет в английском словаре.
Предлагаемый перевод: {word_autotranslation}. Вы согласны с этим переводом (Y/N)? ''')
            if translation_accept == 'Y':
                return admin_or_not(user, word, word_autotranslation)
            if translation_accept == 'N':
                word_translation = input('Введите собственный перевод на русский: ')
                return admin_or_not(user, word, word_translation)

        # слово есть в общем словаре, спрашиваем, устраивает ли пользователя перевод слова
        dict_translation = word_exist.translation_rus
        other_translation = input(f'Перевод: {dict_translation}. Изменить перевод слова (Y/N)? ')

        # пользователь согласен с предложенным вариантом перевода
        if other_translation == 'N':
            insertion = user_engdict_insert(word, user)
            return f'{insertion}, перевод: {dict_translation}.'

        # пользователь не согласен с предложенным вариантом перевода и хочет добавить собственный перевод
        if other_translation == 'Y':
            word_translation = input('Введите свой вариант перевода: ')
            return admin_or_not(user, word, word_translation)


def admin_or_not(user, word, translation):
    user_exist = User.query.filter(User.username == user).first()
    word_exist = EnglishWord.query.filter(EnglishWord.word_itself == word).first()

    # пользователь - не админ, слово добавляется в альтернативный словарь (словарь, генерируемый пользователями)
    if not user_exist.is_admin:
        user_new_word = EnglishWordOfUser(
            word_itself=word,
            user=user,
            translation_rus=translation,
            transcription=get_transcription(word),
            imported_time=datetime.now()
            )
        db.session.add(user_new_word)
        db.session.commit()
        insertion = user_engdict_own_insert(word, user)
        return f'{insertion} и в словарь на сайте, перевод: {translation}.'

    # слова нет в общем словаре (пользователь-админ), слово добавляется в общий словарь
    if not word_exist:
        new_word = EnglishWord(
                word_itself=word,
                translation_rus=translation,
                transcription=get_transcription(word),
                imported_time=datetime.now()
                )
        db.session.add(new_word)
        db.session.commit()
        insertion = user_engdict_insert(word, user)
        return f'{insertion} и в словарь на сайте, перевод: {translation}.'

    # слово есть в общем словаре и его надо заменить (пользователь-админ)
    word_exist.translation_rus = translation
    db.session.commit()
    insertion = user_engdict_insert(word, user)
    return f'{insertion}, перевод: {translation}.'


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
