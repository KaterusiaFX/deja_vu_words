import re
from translate import Translator

from webapp.dictionary.models import EnglishWord, EnglishWordOfUser, FrenchWord, FrenchWordOfUser, UsersWords


def process_user_engdict_index(username):
    user_id = username.id
    user_words = UsersWords.query.filter_by(user_id=user_id).all()
    english_words, english_words_status, english_words_date = [], [], []
    for user_word in user_words:
        if user_word.engword_id:
            eng_word = EnglishWord.query.filter_by(id=user_word.engword_id).first()
        elif user_word.user_engword_id:
            eng_word = EnglishWordOfUser.query.filter_by(id=user_word.user_engword_id).first()
        else:
            eng_word = None
        if eng_word:
            english_words.append(eng_word)
            english_words_status.append(user_word.status)
            english_words_date.append(user_word.imported_time)
    return list(zip(english_words, english_words_status, english_words_date))


def user_engdict_search(word_in_form, username):
    user_id = username.id
    user_words = UsersWords.query.filter_by(user_id=user_id).all()
    word, user_english_word_status, user_english_word_date = None, None, None
    if re.fullmatch("[a-zA-Z]+", word_in_form):
        word_exist_userdict = EnglishWordOfUser.query.filter_by(word_itself=word_in_form).all()
        word_exist = EnglishWord.query.filter_by(word_itself=word_in_form).first()
        for userword in user_words:
            if word_exist and userword.engword_id == word_exist.id:
                word = word_exist
                user_english_word_status, user_english_word_date = userword.status, userword.imported_time
            elif word_exist_userdict:
                for every_word in word_exist_userdict:
                    if every_word.user == username.username and every_word.id == userword.user_engword_id:
                        word = every_word
                        user_english_word_status, user_english_word_date = userword.status, userword.imported_time
    elif re.fullmatch("[а-яА-Я]+", word_in_form):
        word_exist_userdict = EnglishWordOfUser.query.filter_by(translation_rus=word_in_form).all()
        word_exist = EnglishWord.query.filter_by(translation_rus=word_in_form).first()
        for userword in user_words:
            if word_exist and userword.engword_id == word_exist.id:
                word = word_exist
                user_english_word_status, user_english_word_date = userword.status, userword.imported_time
            elif word_exist_userdict:
                for every_word in word_exist_userdict:
                    if every_word.user == username.username and every_word.id == userword.user_engword_id:
                        word = every_word
                        user_english_word_status, user_english_word_date = userword.status, userword.imported_time
    return word, user_english_word_status, user_english_word_date


def user_engdict_translate(word_in_form):
    translation = None
    if re.fullmatch("[a-zA-Z]+", word_in_form):
        word_exist = EnglishWord.query.filter_by(word_itself=word_in_form).first()
        if word_exist:
            translation = word_exist.translation_rus
        else:
            translator = Translator(to_lang="ru")
            translation = translator.translate(word_in_form)
        return translation
    elif re.fullmatch("[а-яА-Я]+", word_in_form):
        word_exist = EnglishWord.query.filter_by(translation_rus=word_in_form).first()
        if word_exist:
            translation = word_exist.word_itself
        else:
            translator = Translator(from_lang='ru', to_lang="en")
            translation = translator.translate(word_in_form)
        return translation


def process_user_frenchdict_index(username):
    user_id = username.id
    user_words = UsersWords.query.filter_by(user_id=user_id).all()
    french_words, french_words_status, french_words_date = [], [], []
    for user_word in user_words:
        if user_word.frenchword_id:
            french_word = FrenchWord.query.filter_by(id=user_word.frenchword_id).first()
        elif user_word.user_frenchword_id:
            french_word = FrenchWordOfUser.query.filter_by(id=user_word.user_frenchword_id).first()
        else:
            french_word = None
        if french_word:
            french_words.append(french_word)
            french_words_status.append(user_word.status)
            french_words_date.append(user_word.imported_time)
    return list(zip(french_words, french_words_status, french_words_date))


def user_frenchdict_search(word_in_form, username):
    user_id = username.id
    user_words = UsersWords.query.filter_by(user_id=user_id).all()
    word, user_french_word_status, user_french_word_date = None, None, None
    if re.fullmatch("[a-zA-Z]+", word_in_form):
        word_exist_userdict = FrenchWordOfUser.query.filter_by(word_itself=word_in_form).all()
        word_exist = FrenchWord.query.filter_by(word_itself=word_in_form).first()
        for userword in user_words:
            if word_exist and userword.frenchword_id == word_exist.id:
                word = word_exist
                user_french_word_status, user_french_word_date = userword.status, userword.imported_time
            elif word_exist_userdict:
                for every_word in word_exist_userdict:
                    if every_word.user == username.username and every_word.id == userword.user_frenchword_id:
                        word = every_word
                        user_french_word_status, user_french_word_date = userword.status, userword.imported_time
    elif re.fullmatch("[а-яА-Я]+", word_in_form):
        word_exist_userdict = FrenchWordOfUser.query.filter_by(translation_rus=word_in_form).all()
        word_exist = FrenchWord.query.filter_by(translation_rus=word_in_form).first()
        for userword in user_words:
            if word_exist and userword.frenchword_id == word_exist.id:
                word = word_exist
                user_french_word_status, user_french_word_date = userword.status, userword.imported_time
            elif word_exist_userdict:
                for every_word in word_exist_userdict:
                    if every_word.user == username.username and every_word.id == userword.user_frenchword_id:
                        word = every_word
                        user_french_word_status, user_french_word_date = userword.status, userword.imported_time
    return word, user_french_word_status, user_french_word_date
