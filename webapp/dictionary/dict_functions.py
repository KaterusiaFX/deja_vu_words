import re

from webapp.dictionary.models import EnglishWord, EnglishWordOfUser, FrenchWord, FrenchWordOfUser, UsersWords


def user_engdict_search(word_in_form, username):
    user_id = username.id
    user_words = UsersWords.query.filter_by(user_id=user_id).all()
    word, user_english_word_status, user_english_word_date = None, None, None
    if re.match("[a-zA-Z]+", word_in_form):
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
    elif re.match("[а-яА-Я]+", word_in_form):
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


def user_frenchdict_search(word_in_form, username):
    user_id = username.id
    user_words = UsersWords.query.filter_by(user_id=user_id).all()
    word, user_french_word_status, user_french_word_date = None, None, None
    if re.match("[a-zA-Z]+", word_in_form):
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
    elif re.match("[а-яА-Я]+", word_in_form):
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
