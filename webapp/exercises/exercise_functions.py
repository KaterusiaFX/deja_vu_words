from datetime import datetime

from webapp.db import db
from webapp.dictionary.dict_functions import user_engdict_search, user_frenchdict_search
from webapp.dictionary.models import UsersWords


def word_status_change_to_familiar(word):
    word.status = 'familiar'
    word.memorizing_time = datetime.now()
    db.session.commit()


def engword_translation_training(username, guess_word, user_answer):
    guess_word = user_engdict_search(guess_word, username)
    word = UsersWords.query.get(guess_word[3])
    if guess_word[0].translation_rus == user_answer:
        word.word_translation = None  # если слово изучено, то в ячейку пишется NULL
        db.session.commit()
        if word.translation_word is None and word.word_write is None \
                and word.translation_write is None and word.remember_word is None:
            word_status_change_to_familiar(word)
        return 'Верно', guess_word
    word.word_translation += 1  # если пользователь ошибся с переводом, то увеличиваем счетчик попыток на 1
    db.session.commit()
    return 'Неверно', guess_word


def translation_engword_training(username, guess_word, user_answer):
    guess_word = user_engdict_search(guess_word, username)
    word = UsersWords.query.get(guess_word[3])
    if guess_word[0].word_itself == user_answer:
        word.translation_word = None
        db.session.commit()
        if word.word_translation is None and word.word_write is None \
                and word.translation_write is None and word.remember_word is None:
            word_status_change_to_familiar(word)
        return 'Верно', guess_word
    word.translation_word += 1
    db.session.commit()
    return 'Неверно', guess_word


def insert_engword_training(username, guess_word, user_answer):
    guess_word = user_engdict_search(guess_word, username)
    word = UsersWords.query.get(guess_word[3])
    if guess_word[0].word_itself == user_answer:
        word.word_write = None
        db.session.commit()
        if word.word_translation is None and word.translation_word is None \
                and word.translation_write is None and word.remember_word is None:
            word_status_change_to_familiar(word)
        return 'Верно', guess_word
    word.word_write += 1
    db.session.commit()
    return 'Неверно', guess_word


def insert_translation_of_engword_training(username, guess_word, user_answer):
    guess_word = user_engdict_search(guess_word, username)
    word = UsersWords.query.get(guess_word[3])
    if guess_word[0].translation_rus == user_answer:
        word.translation_write = None
        db.session.commit()
        if word.word_translation is None and word.translation_word is None \
                and word.word_write is None and word.remember_word is None:
            word_status_change_to_familiar(word)
        return 'Верно', guess_word
    word.translation_write += 1
    db.session.commit()
    return 'Неверно', guess_word


def frenchword_translation_training(username, guess_word, user_answer):
    guess_word = user_frenchdict_search(guess_word, username)
    word = UsersWords.query.get(guess_word[3])
    if guess_word[0].translation_rus == user_answer:
        word.word_translation = None
        db.session.commit()
        if word.translation_word is None and word.word_write is None \
                and word.translation_write is None and word.remember_word is None:
            word_status_change_to_familiar(word)
        return 'Верно', guess_word
    word.word_translation += 1
    db.session.commit()
    return 'Неверно', guess_word


def translation_frenchword_training(username, guess_word, user_answer):
    guess_word = user_frenchdict_search(guess_word, username)
    word = UsersWords.query.get(guess_word[3])
    if guess_word[0].word_itself == user_answer:
        word.translation_word = None
        db.session.commit()
        if word.word_translation is None and word.word_write is None \
                and word.translation_write is None and word.remember_word is None:
            word_status_change_to_familiar(word)
        return 'Верно', guess_word
    word.translation_word += 1
    db.session.commit()
    return 'Неверно', guess_word


def insert_frenchword_training(username, guess_word, user_answer):
    guess_word = user_frenchdict_search(guess_word, username)
    word = UsersWords.query.get(guess_word[3])
    if guess_word[0].word_itself == user_answer:
        word.word_write = None
        db.session.commit()
        if word.word_translation is None and word.translation_word is None \
                and word.translation_write is None and word.remember_word is None:
            word_status_change_to_familiar(word)
        return 'Верно', guess_word
    word.word_write += 1
    db.session.commit()
    return 'Неверно', guess_word


def insert_translation_of_frenchword_training(username, guess_word, user_answer):
    guess_word = user_frenchdict_search(guess_word, username)
    word = UsersWords.query.get(guess_word[3])
    if guess_word[0].translation_rus == user_answer:
        word.translation_write = None
        db.session.commit()
        if word.word_translation is None and word.translation_word is None \
                and word.word_write is None and word.remember_word is None:
            word_status_change_to_familiar(word)
        return 'Верно', guess_word
    word.translation_write += 1
    db.session.commit()
    return 'Неверно', guess_word
