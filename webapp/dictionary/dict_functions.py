import re

from datetime import datetime
from translate import Translator

from webapp.db import db
from webapp.dictionary.get_transcription import get_transcription
from webapp.dictionary.models import EnglishWord, EnglishWordOfUser, FrenchWord, FrenchWordOfUser, UsersWords


def language_check(word):
    if re.fullmatch('[a-zA-Z- ]+', word):
        return 'English'
    if re.fullmatch('[a-zA-ZÀ-ÿÆæŒœ -]+', word):
        return 'French'
    if re.fullmatch('[а-яА-Я- ]+', word):
        return 'Russian'


def process_user_engdict_index(username):
    user_words = UsersWords.query.filter_by(user_id=username.id).all()
    english_words, english_words_status, english_words_date, userword_id, memorizing_date = [], [], [], [], []
    word_translation, translation_word, word_write, translation_write, remember_word = [], [], [], [], []
    for user_word in user_words:
        eng_word = None
        if user_word.engword_id:
            eng_word = EnglishWord.query.filter_by(id=user_word.engword_id).first()
        elif user_word.user_engword_id:
            eng_word = EnglishWordOfUser.query.filter_by(id=user_word.user_engword_id).first()
        if eng_word:
            english_words.append(eng_word)
            english_words_status.append(user_word.status)
            english_words_date.append(user_word.imported_time)
            userword_id.append(user_word.id)
            memorizing_date.append(user_word.memorizing_time)
            word_translation.append(user_word.word_translation)
            translation_word.append(user_word.translation_word)
            word_write.append(user_word.word_write)
            translation_write.append(user_word.translation_write)
            remember_word.append(user_word.remember_word)
    result = list(zip(
        english_words,
        english_words_status,
        english_words_date,
        userword_id,
        memorizing_date,
        word_translation,
        translation_word,
        word_write,
        translation_write,
        remember_word
        ))
    result.reverse()
    return result


def user_engdict_search(word_in_form, username):
    word, user_english_word_status, user_english_word_date, userword_id = None, None, None, None
    user_engwords = process_user_engdict_index(username)

    if language_check(word_in_form) == 'English':
        for engword in user_engwords:
            if engword[0].word_itself == word_in_form:
                return engword[:4]

    elif language_check(word_in_form) == 'Russian':
        for engword in user_engwords:
            if engword[0].translation_rus == word_in_form:
                return engword[:4]

    return word, user_english_word_status, user_english_word_date, userword_id


def user_engdict_translate(word_in_form):
    if language_check(word_in_form) == 'English':
        word_exist = EnglishWord.query.filter_by(word_itself=word_in_form).first()
        if word_exist:
            return word_exist.translation_rus
        translator = Translator(to_lang='ru')
        return translator.translate(word_in_form)

    elif language_check(word_in_form) == 'Russian':
        word_exist = EnglishWord.query.filter_by(translation_rus=word_in_form).first()
        if word_exist:
            return word_exist.word_itself
        translator = Translator(from_lang='ru', to_lang='en')
        return translator.translate(word_in_form)


def user_engdict_add_word(word_in_form, word, username):
    if language_check(word) == 'English':
        # a user wants to add its own translation
        if word_in_form:
            user_new_word = alternative_engdict_supplement(word, username, word_in_form)
            user_engdict_own_insert(user_new_word, username)
            return word, word_in_form
        word_exist = EnglishWord.query.filter_by(word_itself=word).first()
        # a user agree with our translation and the word is in our common dictionary
        if word_exist:
            user_engdict_insert(word_exist, username)
            return word, word_exist.translation_rus
        # a user agree with our translation, but there is no such a word in our common dictionary
        translation = user_engdict_translate(word)
        user_new_word = alternative_engdict_supplement(word, username, translation)
        user_engdict_own_insert(user_new_word, username)
        return word, translation

    elif language_check(word) == 'Russian':
        # a user wants to add its own translation
        if word_in_form:
            user_new_word = alternative_engdict_supplement(word_in_form, username, word)
            user_engdict_own_insert(user_new_word, username)
            return word_in_form, word
        word_exist = EnglishWord.query.filter_by(translation_rus=word).first()
        # a user agree with our translation and the word is in our common dictionary
        if word_exist:
            user_engdict_insert(word_exist, username)
            return word_exist.word_itself, word
        # a user agree with our translation, but there is no such a word in our common dictionary
        translation = user_engdict_translate(word)
        user_new_word = alternative_engdict_supplement(translation, username, word)
        user_engdict_own_insert(user_new_word, username)
        return translation, word


def alternative_engdict_supplement(word, user, translation):
    user_new_word = EnglishWordOfUser(
        word_itself=word,
        user=user.username,
        translation_rus=translation,
        transcription=get_transcription(word),
        imported_time=datetime.now()
        )
    db.session.add(user_new_word)
    db.session.commit()
    return user_new_word


def user_engdict_insert(word, user):
    user.english_words.append(word)
    db.session.add(user)
    db.session.commit()


def user_engdict_own_insert(word, user):
    user.user_english_words.append(word)
    db.session.add(user)
    db.session.commit()


def user_engdict_delete_word(word_in_form, username):
    user_words = UsersWords.query.filter_by(user_id=username.id).all()
    word = None

    if language_check(word_in_form) == 'English':
        word_exist_userdict = EnglishWordOfUser.query.filter_by(word_itself=word_in_form).all()
        word_exist = EnglishWord.query.filter_by(word_itself=word_in_form).first()
        for userword in user_words:
            if word_exist and userword.engword_id == word_exist.id:
                word, deletion, delete_englishwordofuser = word_exist, userword, None
            elif word_exist_userdict:
                for every_word in word_exist_userdict:
                    if every_word.user == username.username and every_word.id == userword.user_engword_id:
                        word, deletion, delete_englishwordofuser = every_word, userword, every_word

    elif language_check(word_in_form) == 'Russian':
        word_exist_userdict = EnglishWordOfUser.query.filter_by(translation_rus=word_in_form).all()
        word_exist = EnglishWord.query.filter_by(translation_rus=word_in_form).first()
        for userword in user_words:
            if word_exist and userword.engword_id == word_exist.id:
                word, deletion, delete_englishwordofuser = word_exist, userword, None
            elif word_exist_userdict:
                for every_word in word_exist_userdict:
                    if every_word.user == username.username and every_word.id == userword.user_engword_id:
                        word, deletion, delete_englishwordofuser = every_word, userword, every_word

    db.session.delete(deletion)
    if delete_englishwordofuser:
        db.session.delete(delete_englishwordofuser)
    db.session.commit()
    return word


def user_engdict_edit_transcription(word_to_edit, transcription, username):
    user_words = UsersWords.query.filter_by(user_id=username.id).all()
    word_exist_userdict = EnglishWordOfUser.query.filter_by(word_itself=word_to_edit).all()
    word_exist = EnglishWord.query.filter_by(word_itself=word_to_edit).first()
    for userword in user_words:
        if word_exist and userword.engword_id == word_exist.id:
            translation = word_exist.translation_rus
            user_engdict_delete_word(word_to_edit, username)
            user_engdict_add_word(translation, word_to_edit, username)
            user_engdict_edit_transcription(word_to_edit, transcription, username)
        elif word_exist_userdict:
            for every_word in word_exist_userdict:
                if every_word.user == username.username and every_word.id == userword.user_engword_id:
                    every_word.transcription = transcription
                    db.session.commit()
                    return


def process_user_frenchdict_index(username):
    user_words = UsersWords.query.filter_by(user_id=username.id).all()
    french_words, french_words_status, french_words_date, userword_id, memorizing_date = [], [], [], [], []
    word_translation, translation_word, word_write, translation_write, remember_word = [], [], [], [], []
    for user_word in user_words:
        french_word = None
        if user_word.frenchword_id:
            french_word = FrenchWord.query.filter_by(id=user_word.frenchword_id).first()
        elif user_word.user_frenchword_id:
            french_word = FrenchWordOfUser.query.filter_by(id=user_word.user_frenchword_id).first()
        if french_word:
            french_words.append(french_word)
            french_words_status.append(user_word.status)
            french_words_date.append(user_word.imported_time)
            userword_id.append(user_word.id)
            memorizing_date.append(user_word.memorizing_time)
            word_translation.append(user_word.word_translation)
            translation_word.append(user_word.translation_word)
            word_write.append(user_word.word_write)
            translation_write.append(user_word.translation_write)
            remember_word.append(user_word.remember_word)
    result = list(zip(
        french_words,
        french_words_status,
        french_words_date,
        userword_id,
        memorizing_date,
        word_translation,
        translation_word,
        word_write,
        translation_write,
        remember_word
        ))
    result.reverse()
    return result


def user_frenchdict_search(word_in_form, username):
    word, user_french_word_status, user_french_word_date, userword_id = None, None, None, None
    user_frenchwords = process_user_frenchdict_index(username)

    if language_check(word_in_form) == 'English' or language_check(word_in_form) == 'French':
        for frenchword in user_frenchwords:
            if frenchword[0].word_itself == word_in_form:
                return frenchword[:4]

    elif language_check(word_in_form) == 'Russian':
        for frenchword in user_frenchwords:
            if frenchword[0].translation_rus == word_in_form:
                return frenchword[:4]

    return word, user_french_word_status, user_french_word_date, userword_id


def user_frenchdict_translate(word_in_form):
    if language_check(word_in_form) == 'English' or language_check(word_in_form) == 'French':
        word_exist = FrenchWord.query.filter_by(word_itself=word_in_form).first()
        if word_exist:
            return word_exist.translation_rus
        translator = Translator(from_lang='fr', to_lang='ru')
        return translator.translate(word_in_form)

    elif language_check(word_in_form) == 'Russian':
        word_exist = FrenchWord.query.filter_by(translation_rus=word_in_form).first()
        if word_exist:
            return word_exist.word_itself
        translator = Translator(from_lang='ru', to_lang='fr')
        return translator.translate(word_in_form)


def user_frenchdict_add_word(word_in_form, word, username):
    if language_check(word) == 'English' or language_check(word) == 'French':
        # a user wants to add its own translation
        if word_in_form:
            user_new_word = alternative_frenchdict_supplement(word, username, word_in_form)
            user_frenchdict_own_insert(user_new_word, username)
            return word, word_in_form
        word_exist = FrenchWord.query.filter_by(word_itself=word).first()
        # a user agree with our translation and the word is in our common dictionary
        if word_exist:
            user_frenchdict_insert(word_exist, username)
            return word, word_exist.translation_rus
        # a user agree with our translation, but there is no such a word in our common dictionary
        translation = user_frenchdict_translate(word)
        user_new_word = alternative_frenchdict_supplement(word, username, translation)
        user_frenchdict_own_insert(user_new_word, username)
        return word, translation

    elif language_check(word) == 'Russian':
        # a user wants to add its own translation
        if word_in_form:
            user_new_word = alternative_frenchdict_supplement(word_in_form, username, word)
            user_frenchdict_own_insert(user_new_word, username)
            return word_in_form, word
        word_exist = FrenchWord.query.filter_by(translation_rus=word).first()
        # a user agree with our translation and the word is in our common dictionary
        if word_exist:
            user_frenchdict_insert(word_exist, username)
            return word_exist.word_itself, word
        # a user agree with our translation, but there is no such a word in our common dictionary
        translation = user_frenchdict_translate(word)
        user_new_word = alternative_frenchdict_supplement(translation, username, word)
        user_frenchdict_own_insert(user_new_word, username)
        return translation, word


def alternative_frenchdict_supplement(word, user, translation):
    user_new_word = FrenchWordOfUser(
        word_itself=word,
        user=user.username,
        translation_rus=translation,
        imported_time=datetime.now()
        )
    db.session.add(user_new_word)
    db.session.commit()
    return user_new_word


def user_frenchdict_insert(word, user):
    user.french_words.append(word)
    db.session.add(user)
    db.session.commit()


def user_frenchdict_own_insert(word, user):
    user.user_french_words.append(word)
    db.session.add(user)
    db.session.commit()


def user_frenchdict_delete_word(word_in_form, username):
    user_words = UsersWords.query.filter_by(user_id=username.id).all()
    word = None

    if language_check(word_in_form) == 'English' or language_check(word_in_form) == 'French':
        word_exist_userdict = FrenchWordOfUser.query.filter_by(word_itself=word_in_form).all()
        word_exist = FrenchWord.query.filter_by(word_itself=word_in_form).first()
        for userword in user_words:
            if word_exist and userword.frenchword_id == word_exist.id:
                word, deletion, delete_frenchwordofuser = word_exist, userword, None
            elif word_exist_userdict:
                for every_word in word_exist_userdict:
                    if every_word.user == username.username and every_word.id == userword.user_frenchword_id:
                        word, deletion, delete_frenchwordofuser = every_word, userword, every_word

    elif language_check(word_in_form) == 'Russian':
        word_exist_userdict = FrenchWordOfUser.query.filter_by(translation_rus=word_in_form).all()
        word_exist = FrenchWord.query.filter_by(translation_rus=word_in_form).first()
        for userword in user_words:
            if word_exist and userword.frenchword_id == word_exist.id:
                word, deletion, delete_frenchwordofuser = word_exist, userword, None
            elif word_exist_userdict:
                for every_word in word_exist_userdict:
                    if every_word.user == username.username and every_word.id == userword.user_frenchword_id:
                        word, deletion, delete_frenchwordofuser = every_word, userword, every_word

    db.session.delete(deletion)
    if delete_frenchwordofuser:
        db.session.delete(delete_frenchwordofuser)
    db.session.commit()
    return word
